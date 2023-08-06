Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const MemberActions = reflux_1.default.createActions([
    'createSuccess',
    'update',
    'updateError',
    'updateSuccess',
    'resendMemberInvite',
    'resendMemberInviteSuccess',
    'resendMemberInviteError',
]);
exports.default = MemberActions;
//# sourceMappingURL=memberActions.jsx.map