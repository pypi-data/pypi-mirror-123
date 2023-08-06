Object.defineProperty(exports, "__esModule", { value: true });
exports.experimentConfig = exports.experimentList = exports.unassignedValue = void 0;
const experiments_1 = require("app/types/experiments");
/**
 * This is the value an experiment will have when the unit of assignment
 * (organization, user, etc) is not part of any experiment group.
 *
 * This likely indicates they should see nothing, or the original version of
 * what's being tested.
 */
exports.unassignedValue = -1;
/**
 * Frontend experiment configuration object
 */
exports.experimentList = [
    {
        key: 'TargetedUpsellModalExperiment',
        type: experiments_1.ExperimentType.Organization,
        parameter: 'exposed',
        assignments: [0, 1],
    },
    {
        key: 'TrialLabelTest',
        type: experiments_1.ExperimentType.Organization,
        parameter: 'exposed',
        assignments: [0, 1],
    },
];
exports.experimentConfig = exports.experimentList.reduce((acc, exp) => (Object.assign(Object.assign({}, acc), { [exp.key]: exp })), {});
//# sourceMappingURL=experimentConfig.jsx.map