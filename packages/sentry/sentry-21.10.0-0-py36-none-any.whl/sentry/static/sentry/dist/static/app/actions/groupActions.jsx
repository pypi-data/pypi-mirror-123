Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
// TODO(dcramer): we should probably just make every parameter update
// work on bulk groups
const GroupActions = reflux_1.default.createActions([
    'assignTo',
    'assignToError',
    'assignToSuccess',
    'delete',
    'deleteError',
    'deleteSuccess',
    'discard',
    'discardError',
    'discardSuccess',
    'update',
    'updateError',
    'updateSuccess',
    'merge',
    'mergeError',
    'mergeSuccess',
    'populateStats',
]);
exports.default = GroupActions;
//# sourceMappingURL=groupActions.jsx.map