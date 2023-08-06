Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const queryString = (0, tslib_1.__importStar)(require("query-string"));
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
const integrationUtil_1 = require("app/utils/integrationUtil");
class AddIntegration extends React.Component {
    constructor() {
        super(...arguments);
        this.dialog = null;
        this.openDialog = (urlParams) => {
            const { account, analyticsParams, modalParams, organization, provider } = this.props;
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.installation_start', Object.assign({ integration: provider.key, integration_type: 'first_party', organization }, analyticsParams));
            const name = 'sentryAddIntegration';
            const { url, width, height } = provider.setupDialog;
            const { left, top } = this.computeCenteredWindow(width, height);
            let query = Object.assign({}, urlParams);
            if (account) {
                query.account = account;
            }
            if (modalParams) {
                query = Object.assign(Object.assign({}, query), modalParams);
            }
            const installUrl = `${url}?${queryString.stringify(query)}`;
            const opts = `scrollbars=yes,width=${width},height=${height},top=${top},left=${left}`;
            this.dialog = window.open(installUrl, name, opts);
            this.dialog && this.dialog.focus();
        };
        this.didReceiveMessage = (message) => {
            const { analyticsParams, onInstall, organization, provider } = this.props;
            if (message.origin !== document.location.origin) {
                return;
            }
            if (message.source !== this.dialog) {
                return;
            }
            const { success, data } = message.data;
            this.dialog = null;
            if (!success) {
                (0, indicator_1.addErrorMessage)(data.error);
                return;
            }
            if (!data) {
                return;
            }
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.installation_complete', Object.assign({ integration: provider.key, integration_type: 'first_party', organization }, analyticsParams));
            (0, indicator_1.addSuccessMessage)((0, locale_1.t)('%s added', provider.name));
            onInstall(data);
        };
    }
    componentDidMount() {
        window.addEventListener('message', this.didReceiveMessage);
    }
    componentWillUnmount() {
        window.removeEventListener('message', this.didReceiveMessage);
        this.dialog && this.dialog.close();
    }
    computeCenteredWindow(width, height) {
        // Taken from: https://stackoverflow.com/questions/4068373/center-a-popup-window-on-screen
        const screenLeft = window.screenLeft !== undefined ? window.screenLeft : window.screenX;
        const screenTop = window.screenTop !== undefined ? window.screenTop : window.screenY;
        const innerWidth = window.innerWidth
            ? window.innerWidth
            : document.documentElement.clientWidth
                ? document.documentElement.clientWidth
                : screen.width;
        const innerHeight = window.innerHeight
            ? window.innerHeight
            : document.documentElement.clientHeight
                ? document.documentElement.clientHeight
                : screen.height;
        const left = innerWidth / 2 - width / 2 + screenLeft;
        const top = innerHeight / 2 - height / 2 + screenTop;
        return { left, top };
    }
    render() {
        const { children } = this.props;
        return children(this.openDialog);
    }
}
exports.default = AddIntegration;
//# sourceMappingURL=addIntegration.jsx.map