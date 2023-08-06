Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const locale_1 = require("app/locale");
const confirmHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/accountSecurity/components/confirmHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const message = (<React.Fragment>
    <confirmHeader_1.default>{(0, locale_1.t)('Do you want to remove this method?')}</confirmHeader_1.default>
    <textBlock_1.default>
      {(0, locale_1.t)('Removing the last authentication method will disable two-factor authentication completely.')}
    </textBlock_1.default>
  </React.Fragment>);
const RemoveConfirm = (props) => <confirm_1.default {...props} message={message}/>;
exports.default = RemoveConfirm;
//# sourceMappingURL=removeConfirm.jsx.map