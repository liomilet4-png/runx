use std::collections::BTreeMap;
use std::fs;
use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};

use runx_contracts::{JsonObject, JsonValue};
use runx_parser::{SkillSource, SourceKind};

use super::profiles::{BUNDLED_VOICE_PROFILE_CONTENT, bundled_profile};
use super::{AgentActInvocationSourceType, build_agent_act_invocation};
use crate::{CredentialDelivery, SkillInvocation};

fn temp_skill(name: &str, body: &str) -> PathBuf {
    let nonce = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("clock")
        .as_nanos();
    let directory = std::env::temp_dir().join(format!("runx-{name}-{nonce}"));
    fs::create_dir_all(&directory).expect("skill directory");
    fs::write(
        directory.join("SKILL.md"),
        format!(
            "---\nname: contract-test\ndescription: Contract test\n---\n\n# Contract test\n\n{body}\n"
        ),
    )
    .expect("skill markdown");
    directory
}

fn invocation(skill_directory: PathBuf, outputs: Option<JsonObject>) -> SkillInvocation {
    SkillInvocation {
        skill_name: "contract-test".to_owned(),
        source: SkillSource {
            source_type: SourceKind::Agent,
            command: None,
            args: Vec::new(),
            cwd: None,
            timeout_seconds: None,
            input_mode: None,
            sandbox: None,
            server: None,
            catalog_ref: None,
            tool: None,
            arguments: None,
            agent_card_url: None,
            agent_identity: None,
            agent: None,
            task: None,
            hook: None,
            outputs,
            graph: None,
            http: None,
            act: None,
            raw: JsonObject::new(),
        },
        inputs: JsonObject::new(),
        resolved_inputs: JsonObject::new(),
        current_context: Vec::new(),
        skill_directory,
        env: BTreeMap::new(),
        credential_delivery: CredentialDelivery::none(),
    }
}

fn outputs() -> JsonObject {
    BTreeMap::from([("plan".to_owned(), JsonValue::String("object".to_owned()))])
}

#[test]
fn bundled_voice_profile_has_content_addressed_identity() {
    let profile = bundled_profile("VOICE.md", BUNDLED_VOICE_PROFILE_CONTENT);

    assert_eq!(profile.content, BUNDLED_VOICE_PROFILE_CONTENT);
    assert!(profile.sha256.as_ref().starts_with("sha256:"));
    assert_eq!(profile.root_path.as_ref(), "runx://profiles");
}

#[test]
fn bundled_voice_profile_matches_canonical_workspace_profile() {
    let canonical = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join("..")
        .join("skills")
        .join("VOICE.md");
    let source = fs::read_to_string(&canonical).expect("canonical skills/VOICE.md");

    assert_eq!(BUNDLED_VOICE_PROFILE_CONTENT, source);
}

#[test]
fn agent_invocation_requires_declared_outputs() {
    let skill = temp_skill(
        "missing-output",
        "Produce one bounded, evidence-backed plan.",
    );
    let request = invocation(skill.clone(), None);

    let error = build_agent_act_invocation(&request, AgentActInvocationSourceType::Agent)
        .expect_err("missing outputs must fail");

    assert!(error.to_string().contains("at least one output"));
    let _ignored = fs::remove_dir_all(skill);
}

#[test]
fn agent_invocation_pins_voice_and_output_contracts() {
    let skill = temp_skill(
        "complete-contract",
        "Produce one bounded, evidence-backed plan.",
    );
    let request = invocation(skill.clone(), Some(outputs()));

    let resolved = build_agent_act_invocation(&request, AgentActInvocationSourceType::Agent)
        .expect("complete contract");

    assert!(resolved.envelope.voice_profile.is_some());
    assert_eq!(resolved.envelope.output.expect("output").len(), 1);
    let _ignored = fs::remove_dir_all(skill);
}
