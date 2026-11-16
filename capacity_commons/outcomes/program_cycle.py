from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from capacity_commons.programs.charter import ContractError, Decision, DomainRecord, RuleResult, bounded, normalized_text
from capacity_commons.curation.coverage_map import grouped_metrics, record_score
from capacity_commons.curation.strata import gate_outcome
from capacity_commons.monitoring.participation_gates import evaluate

STATES = ['proposed', 'funded', 'enrolling', 'delivering', 'evaluated', 'archived']
TRANSITIONS = {state: tuple(STATES[i + 1:i + 3]) for i, state in enumerate(STATES)}

@dataclass(frozen=True)
class TransitionPlan:
    from_state: str
    to_state: str
    allowed: bool
    reasons: tuple[str, ...]
    score: float

def allowed_targets(state: str) -> tuple[str, ...]:
    if state not in TRANSITIONS:
        raise ContractError('unknown workflow state')
    return TRANSITIONS[state]

def plan_transition(record: DomainRecord, target: str, context: Mapping[str, Any] | None = None) -> TransitionPlan:
    context = context or {}
    if target not in STATES:
        raise ContractError('unknown target state')
    scorecard = record_score(record, context)
    reasons: list[str] = []
    structurally_allowed = target in allowed_targets(record.state)
    if not structurally_allowed:
        reasons.append('transition is not adjacent in the lifecycle')
    threshold = float(context.get('transition_threshold', 0.42))
    if scorecard['score'] < threshold:
        reasons.append('record score is below the transition threshold')
    return TransitionPlan(record.state, target, structurally_allowed and not reasons, tuple(reasons or ['eligible']), scorecard['score'])

def apply_transition(record: DomainRecord, target: str, context: Mapping[str, Any] | None = None) -> DomainRecord:
    plan = plan_transition(record, target, context)
    if not plan.allowed:
        raise ContractError('; '.join(plan.reasons))
    return record.with_state(target)

def guard_country_code_sensor_alignment_01(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sensor_alignment', 0.0)
    floor = float(context.get('guard_country_code_sensor_alignment_01_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_code_sensor_alignment_01' + (':passed' if allowed else ':blocked')

def guard_program_track_condition_coverage_02(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('condition_coverage', 0.0)
    floor = float(context.get('guard_program_track_condition_coverage_02_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_program_track_condition_coverage_02' + (':passed' if allowed else ':blocked')

def guard_training_hours_sequence_integrity_03(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sequence_integrity', 0.0)
    floor = float(context.get('guard_training_hours_sequence_integrity_03_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_training_hours_sequence_integrity_03' + (':passed' if allowed else ':blocked')

def guard_participant_count_operator_balance_04(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('operator_balance', 0.0)
    floor = float(context.get('guard_participant_count_operator_balance_04_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_participant_count_operator_balance_04' + (':passed' if allowed else ':blocked')

def guard_completion_rate_quarantine_pressure_05(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('quarantine_pressure', 0.0)
    floor = float(context.get('guard_completion_rate_quarantine_pressure_05_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_completion_rate_quarantine_pressure_05' + (':passed' if allowed else ':blocked')

def guard_localization_score_dataset_novelty_06(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('dataset_novelty', 0.0)
    floor = float(context.get('guard_localization_score_dataset_novelty_06_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_localization_score_dataset_novelty_06' + (':passed' if allowed else ':blocked')

def guard_mentor_coverage_grants_completeness_07(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('grants_completeness', 0.0)
    floor = float(context.get('guard_mentor_coverage_grants_completeness_07_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_mentor_coverage_grants_completeness_07' + (':passed' if allowed else ':blocked')

def guard_platform_uptime_reuse_readiness_08(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reuse_readiness', 0.0)
    floor = float(context.get('guard_platform_uptime_reuse_readiness_08_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_platform_uptime_reuse_readiness_08' + (':passed' if allowed else ':blocked')

def guard_resource_units_sensor_alignment_09(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sensor_alignment', 0.0)
    floor = float(context.get('guard_resource_units_sensor_alignment_09_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_resource_units_sensor_alignment_09' + (':passed' if allowed else ':blocked')

def guard_inclusion_rate_condition_coverage_10(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('condition_coverage', 0.0)
    floor = float(context.get('guard_inclusion_rate_condition_coverage_10_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_inclusion_rate_condition_coverage_10' + (':passed' if allowed else ':blocked')

def guard_partner_code_sequence_integrity_11(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sequence_integrity', 0.0)
    floor = float(context.get('guard_partner_code_sequence_integrity_11_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_partner_code_sequence_integrity_11' + (':passed' if allowed else ':blocked')

def guard_consent_scope_operator_balance_12(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('operator_balance', 0.0)
    floor = float(context.get('guard_consent_scope_operator_balance_12_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consent_scope_operator_balance_12' + (':passed' if allowed else ':blocked')

def guard_country_code_quarantine_pressure_13(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('quarantine_pressure', 0.0)
    floor = float(context.get('guard_country_code_quarantine_pressure_13_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_code_quarantine_pressure_13' + (':passed' if allowed else ':blocked')

def guard_program_track_dataset_novelty_14(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('dataset_novelty', 0.0)
    floor = float(context.get('guard_program_track_dataset_novelty_14_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_program_track_dataset_novelty_14' + (':passed' if allowed else ':blocked')

def guard_training_hours_grants_completeness_15(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('grants_completeness', 0.0)
    floor = float(context.get('guard_training_hours_grants_completeness_15_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_training_hours_grants_completeness_15' + (':passed' if allowed else ':blocked')

def guard_participant_count_reuse_readiness_16(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reuse_readiness', 0.0)
    floor = float(context.get('guard_participant_count_reuse_readiness_16_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_participant_count_reuse_readiness_16' + (':passed' if allowed else ':blocked')

def guard_completion_rate_sensor_alignment_17(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sensor_alignment', 0.0)
    floor = float(context.get('guard_completion_rate_sensor_alignment_17_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_completion_rate_sensor_alignment_17' + (':passed' if allowed else ':blocked')

def guard_localization_score_condition_coverage_18(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('condition_coverage', 0.0)
    floor = float(context.get('guard_localization_score_condition_coverage_18_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_localization_score_condition_coverage_18' + (':passed' if allowed else ':blocked')

def guard_mentor_coverage_sequence_integrity_19(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sequence_integrity', 0.0)
    floor = float(context.get('guard_mentor_coverage_sequence_integrity_19_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_mentor_coverage_sequence_integrity_19' + (':passed' if allowed else ':blocked')

def guard_platform_uptime_operator_balance_20(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('operator_balance', 0.0)
    floor = float(context.get('guard_platform_uptime_operator_balance_20_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_platform_uptime_operator_balance_20' + (':passed' if allowed else ':blocked')

def guard_resource_units_quarantine_pressure_21(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('quarantine_pressure', 0.0)
    floor = float(context.get('guard_resource_units_quarantine_pressure_21_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_resource_units_quarantine_pressure_21' + (':passed' if allowed else ':blocked')

def guard_inclusion_rate_dataset_novelty_22(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('dataset_novelty', 0.0)
    floor = float(context.get('guard_inclusion_rate_dataset_novelty_22_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_inclusion_rate_dataset_novelty_22' + (':passed' if allowed else ':blocked')

def guard_partner_code_grants_completeness_23(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('grants_completeness', 0.0)
    floor = float(context.get('guard_partner_code_grants_completeness_23_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_partner_code_grants_completeness_23' + (':passed' if allowed else ':blocked')

def guard_consent_scope_reuse_readiness_24(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reuse_readiness', 0.0)
    floor = float(context.get('guard_consent_scope_reuse_readiness_24_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consent_scope_reuse_readiness_24' + (':passed' if allowed else ':blocked')

def guard_country_code_sensor_alignment_25(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sensor_alignment', 0.0)
    floor = float(context.get('guard_country_code_sensor_alignment_25_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_code_sensor_alignment_25' + (':passed' if allowed else ':blocked')

def guard_program_track_condition_coverage_26(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('condition_coverage', 0.0)
    floor = float(context.get('guard_program_track_condition_coverage_26_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_program_track_condition_coverage_26' + (':passed' if allowed else ':blocked')

def guard_training_hours_sequence_integrity_27(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sequence_integrity', 0.0)
    floor = float(context.get('guard_training_hours_sequence_integrity_27_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_training_hours_sequence_integrity_27' + (':passed' if allowed else ':blocked')

def guard_participant_count_operator_balance_28(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('operator_balance', 0.0)
    floor = float(context.get('guard_participant_count_operator_balance_28_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_participant_count_operator_balance_28' + (':passed' if allowed else ':blocked')

def guard_completion_rate_quarantine_pressure_29(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('quarantine_pressure', 0.0)
    floor = float(context.get('guard_completion_rate_quarantine_pressure_29_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_completion_rate_quarantine_pressure_29' + (':passed' if allowed else ':blocked')

def guard_localization_score_dataset_novelty_30(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('dataset_novelty', 0.0)
    floor = float(context.get('guard_localization_score_dataset_novelty_30_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_localization_score_dataset_novelty_30' + (':passed' if allowed else ':blocked')

def guard_mentor_coverage_grants_completeness_31(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('grants_completeness', 0.0)
    floor = float(context.get('guard_mentor_coverage_grants_completeness_31_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_mentor_coverage_grants_completeness_31' + (':passed' if allowed else ':blocked')

def guard_platform_uptime_reuse_readiness_32(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reuse_readiness', 0.0)
    floor = float(context.get('guard_platform_uptime_reuse_readiness_32_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_platform_uptime_reuse_readiness_32' + (':passed' if allowed else ':blocked')

def guard_resource_units_sensor_alignment_33(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sensor_alignment', 0.0)
    floor = float(context.get('guard_resource_units_sensor_alignment_33_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_resource_units_sensor_alignment_33' + (':passed' if allowed else ':blocked')

def guard_inclusion_rate_condition_coverage_34(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('condition_coverage', 0.0)
    floor = float(context.get('guard_inclusion_rate_condition_coverage_34_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_inclusion_rate_condition_coverage_34' + (':passed' if allowed else ':blocked')

def guard_partner_code_sequence_integrity_35(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sequence_integrity', 0.0)
    floor = float(context.get('guard_partner_code_sequence_integrity_35_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_partner_code_sequence_integrity_35' + (':passed' if allowed else ':blocked')

def guard_consent_scope_operator_balance_36(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('operator_balance', 0.0)
    floor = float(context.get('guard_consent_scope_operator_balance_36_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consent_scope_operator_balance_36' + (':passed' if allowed else ':blocked')

def guard_country_code_quarantine_pressure_37(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('quarantine_pressure', 0.0)
    floor = float(context.get('guard_country_code_quarantine_pressure_37_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_code_quarantine_pressure_37' + (':passed' if allowed else ':blocked')

def guard_program_track_dataset_novelty_38(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('dataset_novelty', 0.0)
    floor = float(context.get('guard_program_track_dataset_novelty_38_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_program_track_dataset_novelty_38' + (':passed' if allowed else ':blocked')

def guard_training_hours_grants_completeness_39(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('grants_completeness', 0.0)
    floor = float(context.get('guard_training_hours_grants_completeness_39_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_training_hours_grants_completeness_39' + (':passed' if allowed else ':blocked')

def guard_participant_count_reuse_readiness_40(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reuse_readiness', 0.0)
    floor = float(context.get('guard_participant_count_reuse_readiness_40_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_participant_count_reuse_readiness_40' + (':passed' if allowed else ':blocked')

def guard_completion_rate_sensor_alignment_41(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sensor_alignment', 0.0)
    floor = float(context.get('guard_completion_rate_sensor_alignment_41_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_completion_rate_sensor_alignment_41' + (':passed' if allowed else ':blocked')

def guard_localization_score_condition_coverage_42(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('condition_coverage', 0.0)
    floor = float(context.get('guard_localization_score_condition_coverage_42_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_localization_score_condition_coverage_42' + (':passed' if allowed else ':blocked')

def guard_mentor_coverage_sequence_integrity_43(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sequence_integrity', 0.0)
    floor = float(context.get('guard_mentor_coverage_sequence_integrity_43_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_mentor_coverage_sequence_integrity_43' + (':passed' if allowed else ':blocked')

def guard_platform_uptime_operator_balance_44(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('operator_balance', 0.0)
    floor = float(context.get('guard_platform_uptime_operator_balance_44_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_platform_uptime_operator_balance_44' + (':passed' if allowed else ':blocked')

def guard_resource_units_quarantine_pressure_45(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('quarantine_pressure', 0.0)
    floor = float(context.get('guard_resource_units_quarantine_pressure_45_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_resource_units_quarantine_pressure_45' + (':passed' if allowed else ':blocked')

def guard_inclusion_rate_dataset_novelty_46(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('dataset_novelty', 0.0)
    floor = float(context.get('guard_inclusion_rate_dataset_novelty_46_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_inclusion_rate_dataset_novelty_46' + (':passed' if allowed else ':blocked')

def guard_partner_code_grants_completeness_47(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('grants_completeness', 0.0)
    floor = float(context.get('guard_partner_code_grants_completeness_47_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_partner_code_grants_completeness_47' + (':passed' if allowed else ':blocked')

def guard_consent_scope_reuse_readiness_48(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reuse_readiness', 0.0)
    floor = float(context.get('guard_consent_scope_reuse_readiness_48_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consent_scope_reuse_readiness_48' + (':passed' if allowed else ':blocked')

def guard_country_code_sensor_alignment_49(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sensor_alignment', 0.0)
    floor = float(context.get('guard_country_code_sensor_alignment_49_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_code_sensor_alignment_49' + (':passed' if allowed else ':blocked')

def guard_program_track_condition_coverage_50(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('condition_coverage', 0.0)
    floor = float(context.get('guard_program_track_condition_coverage_50_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_program_track_condition_coverage_50' + (':passed' if allowed else ':blocked')

def guard_training_hours_sequence_integrity_51(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sequence_integrity', 0.0)
    floor = float(context.get('guard_training_hours_sequence_integrity_51_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_training_hours_sequence_integrity_51' + (':passed' if allowed else ':blocked')

def guard_participant_count_operator_balance_52(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('operator_balance', 0.0)
    floor = float(context.get('guard_participant_count_operator_balance_52_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_participant_count_operator_balance_52' + (':passed' if allowed else ':blocked')

def guard_completion_rate_quarantine_pressure_53(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('quarantine_pressure', 0.0)
    floor = float(context.get('guard_completion_rate_quarantine_pressure_53_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_completion_rate_quarantine_pressure_53' + (':passed' if allowed else ':blocked')

def guard_localization_score_dataset_novelty_54(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('dataset_novelty', 0.0)
    floor = float(context.get('guard_localization_score_dataset_novelty_54_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_localization_score_dataset_novelty_54' + (':passed' if allowed else ':blocked')

def guard_mentor_coverage_grants_completeness_55(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('grants_completeness', 0.0)
    floor = float(context.get('guard_mentor_coverage_grants_completeness_55_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_mentor_coverage_grants_completeness_55' + (':passed' if allowed else ':blocked')

def guard_platform_uptime_reuse_readiness_56(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reuse_readiness', 0.0)
    floor = float(context.get('guard_platform_uptime_reuse_readiness_56_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_platform_uptime_reuse_readiness_56' + (':passed' if allowed else ':blocked')

def guard_resource_units_sensor_alignment_57(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sensor_alignment', 0.0)
    floor = float(context.get('guard_resource_units_sensor_alignment_57_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_resource_units_sensor_alignment_57' + (':passed' if allowed else ':blocked')

def guard_inclusion_rate_condition_coverage_58(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('condition_coverage', 0.0)
    floor = float(context.get('guard_inclusion_rate_condition_coverage_58_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_inclusion_rate_condition_coverage_58' + (':passed' if allowed else ':blocked')

def guard_partner_code_sequence_integrity_59(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sequence_integrity', 0.0)
    floor = float(context.get('guard_partner_code_sequence_integrity_59_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_partner_code_sequence_integrity_59' + (':passed' if allowed else ':blocked')

def guard_consent_scope_operator_balance_60(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('operator_balance', 0.0)
    floor = float(context.get('guard_consent_scope_operator_balance_60_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consent_scope_operator_balance_60' + (':passed' if allowed else ':blocked')

def guard_country_code_quarantine_pressure_61(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('quarantine_pressure', 0.0)
    floor = float(context.get('guard_country_code_quarantine_pressure_61_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_code_quarantine_pressure_61' + (':passed' if allowed else ':blocked')

def guard_program_track_dataset_novelty_62(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('dataset_novelty', 0.0)
    floor = float(context.get('guard_program_track_dataset_novelty_62_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_program_track_dataset_novelty_62' + (':passed' if allowed else ':blocked')

def guard_training_hours_grants_completeness_63(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('grants_completeness', 0.0)
    floor = float(context.get('guard_training_hours_grants_completeness_63_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_training_hours_grants_completeness_63' + (':passed' if allowed else ':blocked')

def guard_participant_count_reuse_readiness_64(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reuse_readiness', 0.0)
    floor = float(context.get('guard_participant_count_reuse_readiness_64_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_participant_count_reuse_readiness_64' + (':passed' if allowed else ':blocked')

def guard_completion_rate_sensor_alignment_65(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sensor_alignment', 0.0)
    floor = float(context.get('guard_completion_rate_sensor_alignment_65_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_completion_rate_sensor_alignment_65' + (':passed' if allowed else ':blocked')

def guard_localization_score_condition_coverage_66(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('condition_coverage', 0.0)
    floor = float(context.get('guard_localization_score_condition_coverage_66_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_localization_score_condition_coverage_66' + (':passed' if allowed else ':blocked')

def guard_mentor_coverage_sequence_integrity_67(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sequence_integrity', 0.0)
    floor = float(context.get('guard_mentor_coverage_sequence_integrity_67_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_mentor_coverage_sequence_integrity_67' + (':passed' if allowed else ':blocked')

def guard_platform_uptime_operator_balance_68(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('operator_balance', 0.0)
    floor = float(context.get('guard_platform_uptime_operator_balance_68_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_platform_uptime_operator_balance_68' + (':passed' if allowed else ':blocked')

def guard_resource_units_quarantine_pressure_69(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('quarantine_pressure', 0.0)
    floor = float(context.get('guard_resource_units_quarantine_pressure_69_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_resource_units_quarantine_pressure_69' + (':passed' if allowed else ':blocked')

def guard_inclusion_rate_dataset_novelty_70(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('dataset_novelty', 0.0)
    floor = float(context.get('guard_inclusion_rate_dataset_novelty_70_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_inclusion_rate_dataset_novelty_70' + (':passed' if allowed else ':blocked')

def guard_partner_code_grants_completeness_71(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('grants_completeness', 0.0)
    floor = float(context.get('guard_partner_code_grants_completeness_71_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_partner_code_grants_completeness_71' + (':passed' if allowed else ':blocked')

def guard_consent_scope_reuse_readiness_72(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reuse_readiness', 0.0)
    floor = float(context.get('guard_consent_scope_reuse_readiness_72_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consent_scope_reuse_readiness_72' + (':passed' if allowed else ':blocked')

def guard_country_code_sensor_alignment_73(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sensor_alignment', 0.0)
    floor = float(context.get('guard_country_code_sensor_alignment_73_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_code_sensor_alignment_73' + (':passed' if allowed else ':blocked')

def guard_program_track_condition_coverage_74(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('condition_coverage', 0.0)
    floor = float(context.get('guard_program_track_condition_coverage_74_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_program_track_condition_coverage_74' + (':passed' if allowed else ':blocked')

def guard_training_hours_sequence_integrity_75(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sequence_integrity', 0.0)
    floor = float(context.get('guard_training_hours_sequence_integrity_75_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_training_hours_sequence_integrity_75' + (':passed' if allowed else ':blocked')

def guard_participant_count_operator_balance_76(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('operator_balance', 0.0)
    floor = float(context.get('guard_participant_count_operator_balance_76_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_participant_count_operator_balance_76' + (':passed' if allowed else ':blocked')

def guard_completion_rate_quarantine_pressure_77(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('quarantine_pressure', 0.0)
    floor = float(context.get('guard_completion_rate_quarantine_pressure_77_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_completion_rate_quarantine_pressure_77' + (':passed' if allowed else ':blocked')

def guard_localization_score_dataset_novelty_78(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('dataset_novelty', 0.0)
    floor = float(context.get('guard_localization_score_dataset_novelty_78_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_localization_score_dataset_novelty_78' + (':passed' if allowed else ':blocked')

def guard_mentor_coverage_grants_completeness_79(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('grants_completeness', 0.0)
    floor = float(context.get('guard_mentor_coverage_grants_completeness_79_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_mentor_coverage_grants_completeness_79' + (':passed' if allowed else ':blocked')

def guard_platform_uptime_reuse_readiness_80(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reuse_readiness', 0.0)
    floor = float(context.get('guard_platform_uptime_reuse_readiness_80_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_platform_uptime_reuse_readiness_80' + (':passed' if allowed else ':blocked')

def guard_resource_units_sensor_alignment_81(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sensor_alignment', 0.0)
    floor = float(context.get('guard_resource_units_sensor_alignment_81_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_resource_units_sensor_alignment_81' + (':passed' if allowed else ':blocked')

def guard_inclusion_rate_condition_coverage_82(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('condition_coverage', 0.0)
    floor = float(context.get('guard_inclusion_rate_condition_coverage_82_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_inclusion_rate_condition_coverage_82' + (':passed' if allowed else ':blocked')

def guard_partner_code_sequence_integrity_83(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sequence_integrity', 0.0)
    floor = float(context.get('guard_partner_code_sequence_integrity_83_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_partner_code_sequence_integrity_83' + (':passed' if allowed else ':blocked')

def guard_consent_scope_operator_balance_84(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('operator_balance', 0.0)
    floor = float(context.get('guard_consent_scope_operator_balance_84_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consent_scope_operator_balance_84' + (':passed' if allowed else ':blocked')

def guard_country_code_quarantine_pressure_85(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('quarantine_pressure', 0.0)
    floor = float(context.get('guard_country_code_quarantine_pressure_85_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_code_quarantine_pressure_85' + (':passed' if allowed else ':blocked')

def guard_program_track_dataset_novelty_86(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('dataset_novelty', 0.0)
    floor = float(context.get('guard_program_track_dataset_novelty_86_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_program_track_dataset_novelty_86' + (':passed' if allowed else ':blocked')

def guard_training_hours_grants_completeness_87(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('grants_completeness', 0.0)
    floor = float(context.get('guard_training_hours_grants_completeness_87_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_training_hours_grants_completeness_87' + (':passed' if allowed else ':blocked')

def guard_participant_count_reuse_readiness_88(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reuse_readiness', 0.0)
    floor = float(context.get('guard_participant_count_reuse_readiness_88_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_participant_count_reuse_readiness_88' + (':passed' if allowed else ':blocked')

def guard_completion_rate_sensor_alignment_89(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sensor_alignment', 0.0)
    floor = float(context.get('guard_completion_rate_sensor_alignment_89_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_completion_rate_sensor_alignment_89' + (':passed' if allowed else ':blocked')

def guard_localization_score_condition_coverage_90(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('condition_coverage', 0.0)
    floor = float(context.get('guard_localization_score_condition_coverage_90_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_localization_score_condition_coverage_90' + (':passed' if allowed else ':blocked')

def guard_mentor_coverage_sequence_integrity_91(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sequence_integrity', 0.0)
    floor = float(context.get('guard_mentor_coverage_sequence_integrity_91_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_mentor_coverage_sequence_integrity_91' + (':passed' if allowed else ':blocked')

def guard_platform_uptime_operator_balance_92(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('operator_balance', 0.0)
    floor = float(context.get('guard_platform_uptime_operator_balance_92_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_platform_uptime_operator_balance_92' + (':passed' if allowed else ':blocked')

def guard_resource_units_quarantine_pressure_93(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('quarantine_pressure', 0.0)
    floor = float(context.get('guard_resource_units_quarantine_pressure_93_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_resource_units_quarantine_pressure_93' + (':passed' if allowed else ':blocked')

def guard_inclusion_rate_dataset_novelty_94(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('dataset_novelty', 0.0)
    floor = float(context.get('guard_inclusion_rate_dataset_novelty_94_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_inclusion_rate_dataset_novelty_94' + (':passed' if allowed else ':blocked')

def guard_partner_code_grants_completeness_95(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('grants_completeness', 0.0)
    floor = float(context.get('guard_partner_code_grants_completeness_95_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_partner_code_grants_completeness_95' + (':passed' if allowed else ':blocked')

def guard_consent_scope_reuse_readiness_96(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reuse_readiness', 0.0)
    floor = float(context.get('guard_consent_scope_reuse_readiness_96_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consent_scope_reuse_readiness_96' + (':passed' if allowed else ':blocked')

def guard_country_code_sensor_alignment_97(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sensor_alignment', 0.0)
    floor = float(context.get('guard_country_code_sensor_alignment_97_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_code_sensor_alignment_97' + (':passed' if allowed else ':blocked')

def guard_program_track_condition_coverage_98(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('condition_coverage', 0.0)
    floor = float(context.get('guard_program_track_condition_coverage_98_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_program_track_condition_coverage_98' + (':passed' if allowed else ':blocked')

def guard_training_hours_sequence_integrity_99(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sequence_integrity', 0.0)
    floor = float(context.get('guard_training_hours_sequence_integrity_99_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_training_hours_sequence_integrity_99' + (':passed' if allowed else ':blocked')

def guard_participant_count_operator_balance_100(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('operator_balance', 0.0)
    floor = float(context.get('guard_participant_count_operator_balance_100_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_participant_count_operator_balance_100' + (':passed' if allowed else ':blocked')

def guard_completion_rate_quarantine_pressure_101(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('quarantine_pressure', 0.0)
    floor = float(context.get('guard_completion_rate_quarantine_pressure_101_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_completion_rate_quarantine_pressure_101' + (':passed' if allowed else ':blocked')

def guard_localization_score_dataset_novelty_102(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('dataset_novelty', 0.0)
    floor = float(context.get('guard_localization_score_dataset_novelty_102_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_localization_score_dataset_novelty_102' + (':passed' if allowed else ':blocked')

def guard_mentor_coverage_grants_completeness_103(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('grants_completeness', 0.0)
    floor = float(context.get('guard_mentor_coverage_grants_completeness_103_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_mentor_coverage_grants_completeness_103' + (':passed' if allowed else ':blocked')

def guard_platform_uptime_reuse_readiness_104(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reuse_readiness', 0.0)
    floor = float(context.get('guard_platform_uptime_reuse_readiness_104_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_platform_uptime_reuse_readiness_104' + (':passed' if allowed else ':blocked')

def guard_resource_units_sensor_alignment_105(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sensor_alignment', 0.0)
    floor = float(context.get('guard_resource_units_sensor_alignment_105_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_resource_units_sensor_alignment_105' + (':passed' if allowed else ':blocked')

def guard_inclusion_rate_condition_coverage_106(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('condition_coverage', 0.0)
    floor = float(context.get('guard_inclusion_rate_condition_coverage_106_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_inclusion_rate_condition_coverage_106' + (':passed' if allowed else ':blocked')

def guard_partner_code_sequence_integrity_107(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sequence_integrity', 0.0)
    floor = float(context.get('guard_partner_code_sequence_integrity_107_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_partner_code_sequence_integrity_107' + (':passed' if allowed else ':blocked')

def guard_consent_scope_operator_balance_108(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('operator_balance', 0.0)
    floor = float(context.get('guard_consent_scope_operator_balance_108_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consent_scope_operator_balance_108' + (':passed' if allowed else ':blocked')

def guard_country_code_quarantine_pressure_109(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('quarantine_pressure', 0.0)
    floor = float(context.get('guard_country_code_quarantine_pressure_109_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_code_quarantine_pressure_109' + (':passed' if allowed else ':blocked')

def guard_program_track_dataset_novelty_110(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('dataset_novelty', 0.0)
    floor = float(context.get('guard_program_track_dataset_novelty_110_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_program_track_dataset_novelty_110' + (':passed' if allowed else ':blocked')

def guard_training_hours_grants_completeness_111(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('grants_completeness', 0.0)
    floor = float(context.get('guard_training_hours_grants_completeness_111_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_training_hours_grants_completeness_111' + (':passed' if allowed else ':blocked')

def guard_participant_count_reuse_readiness_112(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reuse_readiness', 0.0)
    floor = float(context.get('guard_participant_count_reuse_readiness_112_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_participant_count_reuse_readiness_112' + (':passed' if allowed else ':blocked')

def guard_completion_rate_sensor_alignment_113(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sensor_alignment', 0.0)
    floor = float(context.get('guard_completion_rate_sensor_alignment_113_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_completion_rate_sensor_alignment_113' + (':passed' if allowed else ':blocked')

def guard_localization_score_condition_coverage_114(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('condition_coverage', 0.0)
    floor = float(context.get('guard_localization_score_condition_coverage_114_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_localization_score_condition_coverage_114' + (':passed' if allowed else ':blocked')

def guard_mentor_coverage_sequence_integrity_115(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('sequence_integrity', 0.0)
    floor = float(context.get('guard_mentor_coverage_sequence_integrity_115_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_mentor_coverage_sequence_integrity_115' + (':passed' if allowed else ':blocked')

def guard_platform_uptime_operator_balance_116(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('operator_balance', 0.0)
    floor = float(context.get('guard_platform_uptime_operator_balance_116_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('funded')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_platform_uptime_operator_balance_116' + (':passed' if allowed else ':blocked')

def guard_resource_units_quarantine_pressure_117(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('quarantine_pressure', 0.0)
    floor = float(context.get('guard_resource_units_quarantine_pressure_117_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('enrolling')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_resource_units_quarantine_pressure_117' + (':passed' if allowed else ':blocked')

def guard_inclusion_rate_dataset_novelty_118(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('dataset_novelty', 0.0)
    floor = float(context.get('guard_inclusion_rate_dataset_novelty_118_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('delivering')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_inclusion_rate_dataset_novelty_118' + (':passed' if allowed else ':blocked')

def guard_partner_code_grants_completeness_119(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('grants_completeness', 0.0)
    floor = float(context.get('guard_partner_code_grants_completeness_119_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('evaluated')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_partner_code_grants_completeness_119' + (':passed' if allowed else ':blocked')

def guard_consent_scope_reuse_readiness_120(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reuse_readiness', 0.0)
    floor = float(context.get('guard_consent_scope_reuse_readiness_120_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('archived')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consent_scope_reuse_readiness_120' + (':passed' if allowed else ':blocked')

GUARDS: tuple[Callable[[DomainRecord, Mapping[str, Any]], tuple[bool, str]], ...] = (
    guard_country_code_sensor_alignment_01,
    guard_program_track_condition_coverage_02,
    guard_training_hours_sequence_integrity_03,
    guard_participant_count_operator_balance_04,
    guard_completion_rate_quarantine_pressure_05,
    guard_localization_score_dataset_novelty_06,
    guard_mentor_coverage_grants_completeness_07,
    guard_platform_uptime_reuse_readiness_08,
    guard_resource_units_sensor_alignment_09,
    guard_inclusion_rate_condition_coverage_10,
    guard_partner_code_sequence_integrity_11,
    guard_consent_scope_operator_balance_12,
    guard_country_code_quarantine_pressure_13,
    guard_program_track_dataset_novelty_14,
    guard_training_hours_grants_completeness_15,
    guard_participant_count_reuse_readiness_16,
    guard_completion_rate_sensor_alignment_17,
    guard_localization_score_condition_coverage_18,
    guard_mentor_coverage_sequence_integrity_19,
    guard_platform_uptime_operator_balance_20,
    guard_resource_units_quarantine_pressure_21,
    guard_inclusion_rate_dataset_novelty_22,
    guard_partner_code_grants_completeness_23,
    guard_consent_scope_reuse_readiness_24,
    guard_country_code_sensor_alignment_25,
    guard_program_track_condition_coverage_26,
    guard_training_hours_sequence_integrity_27,
    guard_participant_count_operator_balance_28,
    guard_completion_rate_quarantine_pressure_29,
    guard_localization_score_dataset_novelty_30,
    guard_mentor_coverage_grants_completeness_31,
    guard_platform_uptime_reuse_readiness_32,
    guard_resource_units_sensor_alignment_33,
    guard_inclusion_rate_condition_coverage_34,
    guard_partner_code_sequence_integrity_35,
    guard_consent_scope_operator_balance_36,
    guard_country_code_quarantine_pressure_37,
    guard_program_track_dataset_novelty_38,
    guard_training_hours_grants_completeness_39,
    guard_participant_count_reuse_readiness_40,
    guard_completion_rate_sensor_alignment_41,
    guard_localization_score_condition_coverage_42,
    guard_mentor_coverage_sequence_integrity_43,
    guard_platform_uptime_operator_balance_44,
    guard_resource_units_quarantine_pressure_45,
    guard_inclusion_rate_dataset_novelty_46,
    guard_partner_code_grants_completeness_47,
    guard_consent_scope_reuse_readiness_48,
    guard_country_code_sensor_alignment_49,
    guard_program_track_condition_coverage_50,
    guard_training_hours_sequence_integrity_51,
    guard_participant_count_operator_balance_52,
    guard_completion_rate_quarantine_pressure_53,
    guard_localization_score_dataset_novelty_54,
    guard_mentor_coverage_grants_completeness_55,
    guard_platform_uptime_reuse_readiness_56,
    guard_resource_units_sensor_alignment_57,
    guard_inclusion_rate_condition_coverage_58,
    guard_partner_code_sequence_integrity_59,
    guard_consent_scope_operator_balance_60,
    guard_country_code_quarantine_pressure_61,
    guard_program_track_dataset_novelty_62,
    guard_training_hours_grants_completeness_63,
    guard_participant_count_reuse_readiness_64,
    guard_completion_rate_sensor_alignment_65,
    guard_localization_score_condition_coverage_66,
    guard_mentor_coverage_sequence_integrity_67,
    guard_platform_uptime_operator_balance_68,
    guard_resource_units_quarantine_pressure_69,
    guard_inclusion_rate_dataset_novelty_70,
    guard_partner_code_grants_completeness_71,
    guard_consent_scope_reuse_readiness_72,
    guard_country_code_sensor_alignment_73,
    guard_program_track_condition_coverage_74,
    guard_training_hours_sequence_integrity_75,
    guard_participant_count_operator_balance_76,
    guard_completion_rate_quarantine_pressure_77,
    guard_localization_score_dataset_novelty_78,
    guard_mentor_coverage_grants_completeness_79,
    guard_platform_uptime_reuse_readiness_80,
    guard_resource_units_sensor_alignment_81,
    guard_inclusion_rate_condition_coverage_82,
    guard_partner_code_sequence_integrity_83,
    guard_consent_scope_operator_balance_84,
    guard_country_code_quarantine_pressure_85,
    guard_program_track_dataset_novelty_86,
    guard_training_hours_grants_completeness_87,
    guard_participant_count_reuse_readiness_88,
    guard_completion_rate_sensor_alignment_89,
    guard_localization_score_condition_coverage_90,
    guard_mentor_coverage_sequence_integrity_91,
    guard_platform_uptime_operator_balance_92,
    guard_resource_units_quarantine_pressure_93,
    guard_inclusion_rate_dataset_novelty_94,
    guard_partner_code_grants_completeness_95,
    guard_consent_scope_reuse_readiness_96,
    guard_country_code_sensor_alignment_97,
    guard_program_track_condition_coverage_98,
    guard_training_hours_sequence_integrity_99,
    guard_participant_count_operator_balance_100,
    guard_completion_rate_quarantine_pressure_101,
    guard_localization_score_dataset_novelty_102,
    guard_mentor_coverage_grants_completeness_103,
    guard_platform_uptime_reuse_readiness_104,
    guard_resource_units_sensor_alignment_105,
    guard_inclusion_rate_condition_coverage_106,
    guard_partner_code_sequence_integrity_107,
    guard_consent_scope_operator_balance_108,
    guard_country_code_quarantine_pressure_109,
    guard_program_track_dataset_novelty_110,
    guard_training_hours_grants_completeness_111,
    guard_participant_count_reuse_readiness_112,
    guard_completion_rate_sensor_alignment_113,
    guard_localization_score_condition_coverage_114,
    guard_mentor_coverage_sequence_integrity_115,
    guard_platform_uptime_operator_balance_116,
    guard_resource_units_quarantine_pressure_117,
    guard_inclusion_rate_dataset_novelty_118,
    guard_partner_code_grants_completeness_119,
    guard_consent_scope_reuse_readiness_120,
)

def guard_report(record: DomainRecord, context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    context = dict(context or {})
    context['_metrics'] = grouped_metrics(record, context)
    results = [guard(record, context) for guard in GUARDS]
    return {'passed': sum(item[0] for item in results), 'failed': sum(not item[0] for item in results),
            'messages': [item[1] for item in results]}

def decide(record: DomainRecord, context: Mapping[str, Any] | None = None) -> Decision:
    context = context or {}
    rules = evaluate(record, context)
    scorecard = record_score(record, context)
    guards = guard_report(record, context)
    effective_score = min(scorecard['score'], float(context.get('domain_signal', 1.0)))
    critical = sum(item.severity == 'critical' for item in rules)
    if float(context.get('equity_gap', 0.0)) > 0.45:
        outcome = 'review'
    elif critical:
        outcome = 'hold'
    elif effective_score >= float(context.get('approve_threshold', 0.62)) and guards['passed'] >= guards['failed']:
        outcome = 'approve'
    elif effective_score >= float(context.get('review_threshold', 0.38)):
        outcome = 'review'
    else:
        outcome = 'reject'
    stratum_evidence = normalized_text(context.get('stratum_evidence', ''))
    outcome = gate_outcome(outcome, stratum_evidence)
    reasons = [f"score={scorecard['score']:.6f}", f"critical={critical}",
               f"guards={guards['passed']}/{guards['passed'] + guards['failed']}"]
    if stratum_evidence:
        reasons.append(f"stratum={context.get('stratum_key', 'unknown')}")
        reasons.append(f"stratum_evidence={stratum_evidence}")
        reasons.append(f"stratum_scope={str(context.get('stratum_scope', ''))[:12]}")
    return Decision(record.record_id, outcome, effective_score, tuple(reasons), rules, scorecard['metrics'])

def advance_for_outcome(record: DomainRecord, decision: Decision) -> DomainRecord:
    current = STATES.index(record.state)
    if decision.outcome == 'approve' and current + 1 < len(STATES):
        return record.with_state(STATES[current + 1])
    if decision.outcome == 'hold' and STATES[-1] != record.state:
        return record.with_state(STATES[-1])
    return record
