/**
 * A component to render a Field (i.e. label + help + form "control"),
 * generally inside of a Panel.
 *
 * This is unconnected to any Form state
 */
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const controlState_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/controlState"));
const fieldControl_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldControl"));
const fieldDescription_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldDescription"));
const fieldErrorReason_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldErrorReason"));
const fieldHelp_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldHelp"));
const fieldLabel_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldLabel"));
const fieldRequiredBadge_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldRequiredBadge"));
const fieldWrapper_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldWrapper"));
const fieldQuestion_1 = (0, tslib_1.__importDefault)(require("./fieldQuestion"));
class Field extends React.Component {
    render() {
        const _a = this.props, { className } = _a, otherProps = (0, tslib_1.__rest)(_a, ["className"]);
        const { controlClassName, alignRight, inline, highlighted, required, visible, disabled, disabledReason, error, flexibleControlStateSize, help, id, isSaving, isSaved, label, hideLabel, stacked, children, style, showHelpInTooltip, } = otherProps;
        const isDisabled = typeof disabled === 'function' ? disabled(this.props) : disabled;
        const isVisible = typeof visible === 'function' ? visible(this.props) : visible;
        let Control;
        if (!isVisible) {
            return null;
        }
        const helpElement = typeof help === 'function' ? help(this.props) : help;
        const controlProps = {
            className: controlClassName,
            inline,
            alignRight,
            disabled: isDisabled,
            disabledReason,
            flexibleControlStateSize,
            help: helpElement,
            errorState: error ? <fieldErrorReason_1.default>{error}</fieldErrorReason_1.default> : null,
            controlState: <controlState_1.default error={error} isSaving={isSaving} isSaved={isSaved}/>,
        };
        // See comments in prop types
        if (children instanceof Function) {
            Control = children(Object.assign(Object.assign({}, otherProps), controlProps));
        }
        else {
            Control = <fieldControl_1.default {...controlProps}>{children}</fieldControl_1.default>;
        }
        return (<fieldWrapper_1.default className={className} inline={inline} stacked={stacked} highlighted={highlighted} hasControlState={!flexibleControlStateSize} style={style}>
        {((label && !hideLabel) || helpElement) && (<fieldDescription_1.default inline={inline} htmlFor={id}>
            {label && !hideLabel && (<fieldLabel_1.default disabled={isDisabled}>
                <span>
                  {label}
                  {required && <fieldRequiredBadge_1.default />}
                </span>
                {helpElement && showHelpInTooltip && (<fieldQuestion_1.default>
                    <questionTooltip_1.default position="top" size="sm" title={helpElement}/>
                  </fieldQuestion_1.default>)}
              </fieldLabel_1.default>)}
            {helpElement && !showHelpInTooltip && (<fieldHelp_1.default stacked={stacked} inline={inline}>
                {helpElement}
              </fieldHelp_1.default>)}
          </fieldDescription_1.default>)}

        {Control}
      </fieldWrapper_1.default>);
    }
}
Field.defaultProps = {
    alignRight: false,
    inline: true,
    disabled: false,
    required: false,
    visible: true,
    showHelpInTooltip: false,
};
exports.default = Field;
//# sourceMappingURL=index.jsx.map