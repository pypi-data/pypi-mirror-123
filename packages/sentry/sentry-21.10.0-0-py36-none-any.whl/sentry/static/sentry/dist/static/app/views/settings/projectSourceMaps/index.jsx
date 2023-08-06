Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
function ProjectSourceMapsContainer(props) {
    const { children, organization, project } = props;
    return React.isValidElement(children)
        ? React.cloneElement(children, { organization, project })
        : null;
}
exports.default = (0, withOrganization_1.default)(ProjectSourceMapsContainer);
//# sourceMappingURL=index.jsx.map