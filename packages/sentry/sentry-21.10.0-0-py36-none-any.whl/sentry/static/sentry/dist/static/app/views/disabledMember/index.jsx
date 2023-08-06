Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const notFound_1 = (0, tslib_1.__importDefault)(require("app/components/errors/notFound"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
// getsentry will add the view
const DisabledMemberComponent = (0, hookOrDefault_1.default)({
    hookName: 'component:disabled-member',
    defaultComponent: () => <notFound_1.default />,
});
exports.default = DisabledMemberComponent;
//# sourceMappingURL=index.jsx.map