Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const platformList_1 = (0, tslib_1.__importDefault)(require("app/components/platformList"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
class ProjectAvatar extends react_1.Component {
    constructor() {
        super(...arguments);
        this.getPlatforms = (project) => {
            // `platform` is a user selectable option that is performed during the onboarding process. The reason why this
            // is not the default is because there currently is no way to update it. Fallback to this if project does not
            // have recent events with a platform.
            if (project && project.platform) {
                return [project.platform];
            }
            return [];
        };
    }
    render() {
        const _a = this.props, { project, hasTooltip, tooltip } = _a, props = (0, tslib_1.__rest)(_a, ["project", "hasTooltip", "tooltip"]);
        return (<tooltip_1.default disabled={!hasTooltip} title={tooltip}>
        <platformList_1.default platforms={this.getPlatforms(project)} {...props} max={1}/>
      </tooltip_1.default>);
    }
}
exports.default = ProjectAvatar;
//# sourceMappingURL=projectAvatar.jsx.map