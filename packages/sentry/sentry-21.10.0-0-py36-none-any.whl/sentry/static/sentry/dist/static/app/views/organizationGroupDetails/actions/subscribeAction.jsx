Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/actions/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const utils_1 = require("../utils");
function SubscribeAction({ disabled, group, onClick }) {
    var _a, _b;
    const canChangeSubscriptionState = !((_b = (_a = group.subscriptionDetails) === null || _a === void 0 ? void 0 : _a.disabled) !== null && _b !== void 0 ? _b : false);
    if (!canChangeSubscriptionState) {
        return null;
    }
    return (<button_1.default disabled={disabled} title={(0, utils_1.getSubscriptionReason)(group, true)} priority={group.isSubscribed ? 'primary' : 'default'} size="zero" label={(0, locale_1.t)('Subscribe')} onClick={onClick} icon={<icons_1.IconBell size="xs"/>}/>);
}
exports.default = SubscribeAction;
//# sourceMappingURL=subscribeAction.jsx.map