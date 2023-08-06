Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const styles_1 = require("./styles");
class Gravatar extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            MD5: undefined,
        };
        this._isMounted = false;
        this.buildGravatarUrl = () => {
            const { gravatarId, remoteSize, placeholder } = this.props;
            let url = configStore_1.default.getConfig().gravatarBaseUrl + '/avatar/';
            const md5 = (0, callIfFunction_1.callIfFunction)(this.state.MD5, gravatarId);
            if (md5) {
                url += md5;
            }
            const query = {
                s: remoteSize || undefined,
                // If gravatar is not found we need the request to return an error,
                // otherwise error handler will not trigger and avatar will not have a display a LetterAvatar backup.
                d: placeholder || '404',
            };
            url += '?' + qs.stringify(query);
            return url;
        };
    }
    componentDidMount() {
        this._isMounted = true;
        Promise.resolve().then(() => (0, tslib_1.__importStar)(require('crypto-js/md5'))).then(mod => mod.default)
            .then(MD5 => {
            if (!this._isMounted) {
                return;
            }
            this.setState({ MD5 });
        });
    }
    componentWillUnmount() {
        // Need to track mounted state because `React.isMounted()` is deprecated and because of
        // dynamic imports
        this._isMounted = false;
    }
    render() {
        if (!this.state.MD5) {
            return null;
        }
        const { round, onError, onLoad, suggested, grayscale } = this.props;
        return (<Image round={round} src={this.buildGravatarUrl()} onLoad={onLoad} onError={onError} suggested={suggested} grayscale={grayscale}/>);
    }
}
exports.default = Gravatar;
const Image = (0, styled_1.default)('img') `
  ${styles_1.imageStyle};
`;
//# sourceMappingURL=gravatar.jsx.map