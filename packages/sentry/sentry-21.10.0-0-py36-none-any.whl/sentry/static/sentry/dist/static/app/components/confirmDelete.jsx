Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const locale_1 = require("app/locale");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const ConfirmDelete = (_a) => {
    var { message, confirmInput } = _a, props = (0, tslib_1.__rest)(_a, ["message", "confirmInput"]);
    return (<confirm_1.default {...props} bypass={false} disableConfirmButton renderMessage={({ disableConfirmButton }) => (<React.Fragment>
        <alert_1.default type="error">{message}</alert_1.default>
        <field_1.default flexibleControlStateSize inline={false} label={(0, locale_1.t)('Please enter %s to confirm the deletion', <code>{confirmInput}</code>)}>
          <input_1.default type="text" placeholder={confirmInput} onChange={e => disableConfirmButton(e.target.value !== confirmInput)}/>
        </field_1.default>
      </React.Fragment>)}/>);
};
exports.default = ConfirmDelete;
//# sourceMappingURL=confirmDelete.jsx.map