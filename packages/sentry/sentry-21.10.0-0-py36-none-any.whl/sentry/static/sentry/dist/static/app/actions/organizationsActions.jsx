Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const OrganizationsActions = reflux_1.default.createActions([
    'update',
    'setActive',
    'changeSlug',
    'remove',
    'removeSuccess',
    'removeError',
]);
exports.default = OrganizationsActions;
//# sourceMappingURL=organizationsActions.jsx.map