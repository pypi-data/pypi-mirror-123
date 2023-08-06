Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const projectDetail_1 = (0, tslib_1.__importDefault)(require("./projectDetail"));
function ProjectDetailContainer(props) {
    return <projectDetail_1.default {...props}/>;
}
exports.default = (0, withOrganization_1.default)(ProjectDetailContainer);
//# sourceMappingURL=index.jsx.map