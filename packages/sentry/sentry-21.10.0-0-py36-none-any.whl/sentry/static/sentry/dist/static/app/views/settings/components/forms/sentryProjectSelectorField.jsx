Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_select_1 = require("react-select");
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const locale_1 = require("app/locale");
const inputField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/inputField"));
const defaultProps = {
    avatarSize: 20,
    placeholder: (0, locale_1.t)('Choose Sentry project'),
};
class RenderField extends React.Component {
    constructor() {
        super(...arguments);
        // need to map the option object to the value
        this.handleChange = (onBlur, onChange, optionObj, event) => {
            const { value } = optionObj;
            onChange === null || onChange === void 0 ? void 0 : onChange(value, event);
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(value, event);
        };
    }
    render() {
        const _a = this.props, { projects, avatarSize, onChange, onBlur } = _a, rest = (0, tslib_1.__rest)(_a, ["projects", "avatarSize", "onChange", "onBlur"]);
        const projectOptions = projects.map(({ slug, id }) => ({ value: id, label: slug }));
        const customOptionProject = projectProps => {
            const project = projects.find(proj => proj.id === projectProps.value);
            // shouldn't happen but need to account for it
            if (!project) {
                return <react_select_1.components.Option {...projectProps}/>;
            }
            return (<react_select_1.components.Option {...projectProps}>
          <idBadge_1.default project={project} avatarSize={avatarSize} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>
        </react_select_1.components.Option>);
        };
        const customValueContainer = containerProps => {
            const selectedValue = containerProps.getValue()[0];
            const project = projects.find(proj => proj.id === (selectedValue === null || selectedValue === void 0 ? void 0 : selectedValue.value));
            // shouldn't happen but need to account for it
            if (!project) {
                return <react_select_1.components.ValueContainer {...containerProps}/>;
            }
            return (<react_select_1.components.ValueContainer {...containerProps}>
          <idBadge_1.default project={project} avatarSize={avatarSize} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>
        </react_select_1.components.ValueContainer>);
        };
        return (<selectControl_1.default options={projectOptions} components={{
                Option: customOptionProject,
                SingleValue: customValueContainer,
            }} {...rest} onChange={this.handleChange.bind(this, onBlur, onChange)}/>);
    }
}
RenderField.defaultProps = defaultProps;
const SentryProjectSelectorField = (props) => (<inputField_1.default {...props} field={(renderProps) => <RenderField {...renderProps}/>}/>);
exports.default = SentryProjectSelectorField;
//# sourceMappingURL=sentryProjectSelectorField.jsx.map