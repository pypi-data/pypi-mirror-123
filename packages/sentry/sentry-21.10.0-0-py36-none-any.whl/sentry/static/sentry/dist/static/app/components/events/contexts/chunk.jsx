Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const locale_1 = require("app/locale");
const plugins_1 = (0, tslib_1.__importDefault)(require("app/plugins"));
const utils_1 = require("app/utils");
const utils_2 = require("./utils");
class Chunk extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isLoading: false,
        };
    }
    UNSAFE_componentWillMount() {
        this.syncPlugin();
    }
    componentDidUpdate(prevProps) {
        var _a, _b;
        if (prevProps.type !== this.props.type ||
            ((_a = prevProps.group) === null || _a === void 0 ? void 0 : _a.id) !== ((_b = this.props.group) === null || _b === void 0 ? void 0 : _b.id)) {
            this.syncPlugin();
        }
    }
    syncPlugin() {
        const { group, type, alias } = this.props;
        // If we don't have a grouped event we can't sync with plugins.
        if (!group) {
            return;
        }
        // Search using `alias` first because old plugins rely on it and type is set to "default"
        // e.g. sessionstack
        const sourcePlugin = type === 'default'
            ? (0, utils_2.getSourcePlugin)(group.pluginContexts, alias) ||
                (0, utils_2.getSourcePlugin)(group.pluginContexts, type)
            : (0, utils_2.getSourcePlugin)(group.pluginContexts, type);
        if (!sourcePlugin) {
            this.setState({ pluginLoading: false });
            return;
        }
        this.setState({
            pluginLoading: true,
        }, () => {
            plugins_1.default.load(sourcePlugin, () => {
                this.setState({ pluginLoading: false });
            });
        });
    }
    getTitle() {
        const { value = {}, alias, type } = this.props;
        if ((0, utils_1.defined)(value.title) && typeof value.title !== 'object') {
            return value.title;
        }
        if (!(0, utils_1.defined)(type)) {
            return (0, utils_1.toTitleCase)(alias);
        }
        switch (type) {
            case 'app':
                return (0, locale_1.t)('App');
            case 'device':
                return (0, locale_1.t)('Device');
            case 'os':
                return (0, locale_1.t)('Operating System');
            case 'user':
                return (0, locale_1.t)('User');
            case 'gpu':
                return (0, locale_1.t)('Graphics Processing Unit');
            case 'runtime':
                return (0, locale_1.t)('Runtime');
            case 'trace':
                return (0, locale_1.t)('Trace Details');
            case 'default':
                if (alias === 'state')
                    return (0, locale_1.t)('Application State');
                return (0, utils_1.toTitleCase)(alias);
            default:
                return (0, utils_1.toTitleCase)(type);
        }
    }
    render() {
        const { pluginLoading } = this.state;
        // if we are currently loading the plugin, just render nothing for now.
        if (pluginLoading) {
            return null;
        }
        const { type, alias, value = {}, event } = this.props;
        // we intentionally hide reprocessing context to not imply it was sent by the SDK.
        if (alias === 'reprocessing') {
            return null;
        }
        const Component = type === 'default'
            ? (0, utils_2.getContextComponent)(alias) || (0, utils_2.getContextComponent)(type)
            : (0, utils_2.getContextComponent)(type);
        const isObjectValueEmpty = Object.values(value).filter(v => (0, utils_1.defined)(v)).length === 0;
        // this can happen if the component does not exist
        if (!Component || isObjectValueEmpty) {
            return null;
        }
        return (<eventDataSection_1.default key={`context-${alias}`} type={`context-${alias}`} title={<React.Fragment>
            {this.getTitle()}
            {(0, utils_1.defined)(type) && type !== 'default' && alias !== type && (<small>({alias})</small>)}
          </React.Fragment>}>
        <Component alias={alias} event={event} data={value}/>
      </eventDataSection_1.default>);
    }
}
exports.default = Chunk;
//# sourceMappingURL=chunk.jsx.map