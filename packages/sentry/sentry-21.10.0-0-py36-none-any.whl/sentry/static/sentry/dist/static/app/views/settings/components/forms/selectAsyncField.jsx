Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const selectAsyncControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectAsyncControl"));
const inputField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/inputField"));
class SelectAsyncField extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            results: [],
        };
        // need to map the option object to the value
        // this is essentially the same code from ./selectField handleChange()
        this.handleChange = (onBlur, onChange, optionObj, event) => {
            let { value } = optionObj;
            if (!optionObj) {
                value = optionObj;
            }
            else if (this.props.multiple && Array.isArray(optionObj)) {
                // List of optionObjs
                value = optionObj.map(({ value: val }) => val);
            }
            else if (!Array.isArray(optionObj)) {
                value = optionObj.value;
            }
            onChange === null || onChange === void 0 ? void 0 : onChange(value, event);
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(value, event);
        };
    }
    findValue(propsValue) {
        /**
         * The propsValue is the `id` of the object (user, team, etc), and
         * react-select expects a full value object: {value: "id", label: "name"}
         *
         * Returning {} here will show the user a dropdown with "No options".
         **/
        return this.state.results.find(({ value }) => value === propsValue) || {};
    }
    render() {
        const otherProps = (0, tslib_1.__rest)(this.props, []);
        return (<inputField_1.default {...otherProps} field={(_a) => {
                var { onChange, onBlur, required: _required, onResults, value } = _a, props = (0, tslib_1.__rest)(_a, ["onChange", "onBlur", "required", "onResults", "value"]);
                return (<selectAsyncControl_1.default {...props} onChange={this.handleChange.bind(this, onBlur, onChange)} onResults={data => {
                        const results = onResults(data);
                        this.setState({ results });
                        return results;
                    }} onSelectResetsInput onCloseResetsInput={false} onBlurResetsInput={false} value={this.findValue(value)}/>);
            }}/>);
    }
}
exports.default = SelectAsyncField;
//# sourceMappingURL=selectAsyncField.jsx.map