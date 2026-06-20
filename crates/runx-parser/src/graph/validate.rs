use std::collections::BTreeSet;

use runx_contracts::JsonObject;

use super::fanout::{validate_fanout_groups, validate_fanout_step_bindings};
use super::helpers::{
    optional_string, required_array, required_object, required_string, validation_error,
};
use super::policy::validate_graph_policy;
use super::step::validate_step;
use super::types::{ExecutionGraph, RawGraphIr};
use crate::{ParseError, ValidationError, assert_yaml_parity_subset};

pub fn parse_graph_yaml(source: &str) -> Result<RawGraphIr, ParseError> {
    assert_yaml_parity_subset("graph", source)?;
    let document: JsonObject =
        serde_norway::from_str(source).map_err(|error| ParseError::InvalidYaml {
            field: "graph".to_owned(),
            message: error.to_string(),
        })?;
    Ok(RawGraphIr { document })
}

pub fn validate_graph(raw: RawGraphIr) -> Result<ExecutionGraph, ValidationError> {
    validate_graph_document(raw.document.clone(), Some(raw))
}

pub fn validate_graph_document(
    document: JsonObject,
    raw: Option<RawGraphIr>,
) -> Result<ExecutionGraph, ValidationError> {
    reject_unsupported_top_level(&document)?;

    let name = required_string(document.get("name"), "name")?;
    let owner = optional_string(document.get("owner"), "owner")?;
    let raw_steps = required_array(document.get("steps"), "steps")?;
    let fanout_groups = validate_fanout_groups(document.get("fanout"), "fanout")?;
    let policy = validate_graph_policy(document.get("policy"), "policy")?;
    let mut seen_step_ids = BTreeSet::new();
    let mut steps = Vec::new();

    for (index, raw_step) in raw_steps.iter().enumerate() {
        let field = format!("steps.{index}");
        let raw_step = required_object(Some(raw_step), &field)?;
        let step = validate_step(raw_step, &field, &seen_step_ids)?;
        seen_step_ids.insert(step.id.clone());
        steps.push(step);
    }

    validate_fanout_step_bindings(&steps, &fanout_groups)?;

    Ok(ExecutionGraph {
        name,
        owner,
        steps,
        fanout_groups,
        policy,
        raw: raw.unwrap_or(RawGraphIr { document }),
    })
}

fn reject_unsupported_top_level(document: &JsonObject) -> Result<(), ValidationError> {
    for field in ["sync", "schedule", "schedules"] {
        if document.contains_key(field) {
            return Err(validation_error(format!(
                "{field} is not supported by the local sequential graph runner."
            )));
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::{parse_graph_yaml, validate_graph};

    #[test]
    fn inputs_reject_previous_step_output_references() -> Result<(), String> {
        let raw = parse_graph_yaml(
            r#"
name: bad-input-ref
steps:
  - id: select
    run:
      type: agent-task
  - id: review
    run:
      type: agent-task
    inputs:
      bounty: select.result
"#,
        )
        .map_err(|error| error.to_string())?;
        let error = validate_graph(raw)
            .err()
            .ok_or_else(|| "graph unexpectedly validated".to_owned())?;
        let message = error.to_string();
        assert!(message.contains("steps.1.inputs.bounty"));
        assert!(message.contains("move it to context"));
        Ok(())
    }

    #[test]
    fn inputs_allow_literals_that_are_not_previous_step_refs() -> Result<(), String> {
        let raw = parse_graph_yaml(
            r#"
name: literal-input
steps:
  - id: review
    run:
      type: agent-task
    inputs:
      literal: select.result
      variable: $input.claim
      url: https://example.com/a.b
"#,
        )
        .map_err(|error| error.to_string())?;
        validate_graph(raw).map_err(|error| error.to_string())?;
        Ok(())
    }
}
