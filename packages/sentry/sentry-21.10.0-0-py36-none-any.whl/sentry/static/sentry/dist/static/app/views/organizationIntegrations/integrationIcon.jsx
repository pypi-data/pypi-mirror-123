Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const pluginIcon_1 = (0, tslib_1.__importStar)(require("app/plugins/components/pluginIcon"));
const StyledIcon = (0, styled_1.default)('img') `
  height: ${p => p.size}px;
  width: ${p => p.size}px;
  border-radius: 2px;
  display: block;
`;
class Icon extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            imgSrc: this.props.integration.icon,
        };
    }
    render() {
        const { integration, size } = this.props;
        return (<StyledIcon size={size} src={this.state.imgSrc} onError={() => {
                this.setState({ imgSrc: pluginIcon_1.ICON_PATHS[integration.provider.key] || pluginIcon_1.DEFAULT_ICON });
            }}/>);
    }
}
const IntegrationIcon = ({ integration, size = 32 }) => integration.icon ? (<Icon size={size} integration={integration}/>) : (<pluginIcon_1.default size={size} pluginId={integration.provider.key}/>);
exports.default = IntegrationIcon;
//# sourceMappingURL=integrationIcon.jsx.map