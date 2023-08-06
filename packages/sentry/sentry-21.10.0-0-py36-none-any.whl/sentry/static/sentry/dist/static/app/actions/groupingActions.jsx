Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
// Actions for "Grouping" view - for merging/unmerging events/issues
const GroupingActions = reflux_1.default.createActions([
    'fetch',
    'showAllSimilarItems',
    'toggleUnmerge',
    'toggleMerge',
    'unmerge',
    'merge',
    'toggleCollapseFingerprint',
    'toggleCollapseFingerprints',
]);
exports.default = GroupingActions;
//# sourceMappingURL=groupingActions.jsx.map