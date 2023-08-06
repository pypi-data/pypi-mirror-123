Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const settingsBreadcrumbActions_1 = (0, tslib_1.__importDefault)(require("app/actions/settingsBreadcrumbActions"));
class BreadcrumbTitle extends react_1.Component {
    componentDidMount() {
        settingsBreadcrumbActions_1.default.mapTitle(this.props);
    }
    render() {
        return null;
    }
}
exports.default = BreadcrumbTitle;
//# sourceMappingURL=breadcrumbTitle.jsx.map