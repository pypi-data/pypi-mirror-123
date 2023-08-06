Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
class SubscribeButton extends React.Component {
    render() {
        const { size, isSubscribed, onClick, disabled } = this.props;
        const icon = <icons_1.IconBell color={isSubscribed ? 'blue300' : undefined}/>;
        return (<button_1.default size={size} icon={icon} onClick={onClick} disabled={disabled}>
        {isSubscribed ? (0, locale_1.t)('Unsubscribe') : (0, locale_1.t)('Subscribe')}
      </button_1.default>);
    }
}
exports.default = SubscribeButton;
//# sourceMappingURL=subscribeButton.jsx.map