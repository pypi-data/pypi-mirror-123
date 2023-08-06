Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const commandLine_1 = (0, tslib_1.__importDefault)(require("app/components/commandLine"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const WaitingActivity = ({ onRefresh, disabled }) => (<panels_1.Panel>
    <emptyMessage_1.default title={(0, locale_1.t)('Waiting on Activity!')} description={disabled
        ? undefined
        : (0, locale_1.tct)('Run relay in your terminal with [commandLine]', {
            commandLine: <commandLine_1.default>{'relay run'}</commandLine_1.default>,
        })} action={<button_1.default icon={<icons_1.IconRefresh />} onClick={onRefresh}>
          {(0, locale_1.t)('Refresh')}
        </button_1.default>}/>
  </panels_1.Panel>);
exports.default = WaitingActivity;
//# sourceMappingURL=waitingActivity.jsx.map