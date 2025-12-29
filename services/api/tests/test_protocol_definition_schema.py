import pytest

from app.modules.protocols.protocol_definition import ProtocolDefinitionSchema, build_protocol_definition_resource


def test_protocol_definition_requires_approval_step():
    with pytest.raises(ValueError):
        ProtocolDefinitionSchema(
            protocolId="kmt-core",
            version="v1",
            title="KMT",
            status="active",
            steps=[
                {
                    "stepId": "note",
                    "title": "Informational",
                    "description": "No approval needed",
                    "approvalRequired": False,
                }
            ],
        )


def test_protocol_definition_builds_actions():
    schema = ProtocolDefinitionSchema(
        protocolId="kmt-core",
        version="v1",
        title="KMT",
        status="active",
        steps=[
            {
                "stepId": "review",
                "title": "Clinician review",
                "description": "Review markers",
                "approvalRequired": True,
            }
        ],
    )
    resource = build_protocol_definition_resource(schema)
    assert resource["resourceType"] == "PlanDefinition"
    assert resource["version"] == "v1"
    assert resource["action"][0]["extension"][0]["valueBoolean"] is True
