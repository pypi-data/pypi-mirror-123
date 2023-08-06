Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_select_1 = require("react-select");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class SelectField extends React.Component {
    constructor() {
        super(...arguments);
        // TODO(ts) The generics in react-select make getting a good type here hard.
        this.selectRef = React.createRef();
    }
    componentDidMount() {
        var _a, _b;
        if (!this.selectRef.current) {
            return;
        }
        if ((_b = (_a = this.selectRef.current) === null || _a === void 0 ? void 0 : _a.select) === null || _b === void 0 ? void 0 : _b.inputRef) {
            this.selectRef.current.select.inputRef.autocomplete = 'off';
        }
    }
    render() {
        return (<selectControl_1.default {...this.props} isSearchable={false} styles={{
                control: (provided) => (Object.assign(Object.assign({}, provided), { minHeight: '41px', height: '41px' })),
            }} ref={this.selectRef} components={{
                Option: (_a) => {
                    var _b = _a.data, { label, description } = _b, data = (0, tslib_1.__rest)(_b, ["label", "description"]), { isSelected } = _a, props = (0, tslib_1.__rest)(_a, ["data", "isSelected"]);
                    return (<react_select_1.components.Option isSelected={isSelected} data={data} {...props}>
              <Wrapper>
                <div data-test-id="label">{label}</div>
                {description && <Description>{`(${description})`}</Description>}
              </Wrapper>
            </react_select_1.components.Option>);
                },
            }} openOnFocus/>);
    }
}
exports.default = SelectField;
const Description = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
`;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr auto;
  grid-gap: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=selectField.jsx.map