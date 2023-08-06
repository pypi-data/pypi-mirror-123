Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const Option = React.forwardRef(function Option({ name, disabled, label, value, checked, onChange }, ref) {
    function handleChange(e) {
        const isTrue = e.target.value === 'true';
        onChange === null || onChange === void 0 ? void 0 : onChange(isTrue, e);
    }
    return (<div className="radio">
      <label style={{ fontWeight: 'normal' }}>
        <input ref={ref} type="radio" value={value} name={name} checked={checked} onChange={handleChange} disabled={disabled}/>{' '}
        {label}
      </label>
    </div>);
});
const RadioBoolean = React.forwardRef(function RadioBoolean({ disabled, name, onChange, value, yesFirst = true, yesLabel = 'Yes', noLabel = 'No', }, ref) {
    const yesOption = (<Option ref={ref} value="true" checked={value === true} name={name} disabled={disabled} label={yesLabel} onChange={onChange}/>);
    const noOption = (<Option value="false" checked={value === false} name={name} disabled={disabled} label={noLabel} onChange={onChange}/>);
    return (<div>
      {yesFirst ? yesOption : noOption}
      {yesFirst ? noOption : yesOption}
    </div>);
});
exports.default = RadioBoolean;
//# sourceMappingURL=radioBoolean.jsx.map