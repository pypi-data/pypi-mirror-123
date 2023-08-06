Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const sanitizeQuerySelector_1 = require("app/utils/sanitizeQuerySelector");
const fieldFromConfig_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/fieldFromConfig"));
class FormPanel extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            collapsed: false,
        };
        this.handleToggleEvents = () => {
            const { collapsed } = this.state;
            this.setState({ collapsed: !collapsed });
        };
    }
    render() {
        const _a = this.props, { title, fields, access, disabled, additionalFieldProps, renderFooter, renderHeader, collapsible } = _a, otherProps = (0, tslib_1.__rest)(_a, ["title", "fields", "access", "disabled", "additionalFieldProps", "renderFooter", "renderHeader", "collapsible"]);
        const { collapsed } = this.state;
        return (<panels_1.Panel id={typeof title === 'string' ? (0, sanitizeQuerySelector_1.sanitizeQuerySelector)(title) : undefined}>
        {title && (<panels_1.PanelHeader>
            {title}
            {collapsible && (<Collapse onClick={this.handleToggleEvents}>
                <icons_1.IconChevron direction={collapsed ? 'down' : 'up'} size="xs"/>
              </Collapse>)}
          </panels_1.PanelHeader>)}
        {!collapsed && (<panels_1.PanelBody>
            {typeof renderHeader === 'function' && renderHeader({ title, fields })}

            {fields.map(field => {
                    if (typeof field === 'function') {
                        return field();
                    }
                    const { defaultValue: _ } = field, fieldWithoutDefaultValue = (0, tslib_1.__rest)(field, ["defaultValue"]);
                    // Allow the form panel disabled prop to override the fields
                    // disabled prop, with fallback to the fields disabled state.
                    if (disabled === true) {
                        fieldWithoutDefaultValue.disabled = true;
                        fieldWithoutDefaultValue.disabledReason = undefined;
                    }
                    return (<fieldFromConfig_1.default access={access} disabled={disabled} key={field.name} {...otherProps} {...additionalFieldProps} field={fieldWithoutDefaultValue} highlighted={this.props.highlighted === `#${field.name}`}/>);
                })}
            {typeof renderFooter === 'function' && renderFooter({ title, fields })}
          </panels_1.PanelBody>)}
      </panels_1.Panel>);
    }
}
exports.default = FormPanel;
FormPanel.defaultProps = {
    additionalFieldProps: {},
};
const Collapse = (0, styled_1.default)('span') `
  cursor: pointer;
`;
//# sourceMappingURL=formPanel.jsx.map