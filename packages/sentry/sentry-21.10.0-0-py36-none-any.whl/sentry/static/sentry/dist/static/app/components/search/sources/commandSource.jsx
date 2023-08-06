Object.defineProperty(exports, "__esModule", { value: true });
exports.CommandSource = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const modal_1 = require("app/actionCreators/modal");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const createFuzzySearch_1 = require("app/utils/createFuzzySearch");
const ACTIONS = [
    {
        title: 'Open Sudo Modal',
        description: 'Open Sudo Modal to re-identify yourself.',
        requiresSuperuser: false,
        action: () => (0, modal_1.openSudo)({
            sudo: true,
        }),
    },
    {
        title: 'Open Superuser Modal',
        description: 'Open Superuser Modal to re-identify yourself.',
        requiresSuperuser: true,
        action: () => (0, modal_1.openSudo)({
            superuser: true,
        }),
    },
    {
        title: 'Toggle dark mode',
        description: 'Toggle dark mode (superuser only atm)',
        requiresSuperuser: true,
        action: () => configStore_1.default.set('theme', configStore_1.default.get('theme') === 'dark' ? 'light' : 'dark'),
    },
    {
        title: 'Toggle Translation Markers',
        description: 'Toggles translation markers on or off in the application',
        requiresSuperuser: true,
        action: () => {
            (0, locale_1.toggleLocaleDebug)();
            window.location.reload();
        },
    },
    {
        title: 'Search Documentation and FAQ',
        description: 'Open the Documentation and FAQ search modal.',
        requiresSuperuser: false,
        action: () => {
            (0, modal_1.openHelpSearchModal)();
        },
    },
];
/**
 * This source is a hardcoded list of action creators and/or routes maybe
 */
class CommandSource extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            fuzzy: null,
        };
    }
    componentDidMount() {
        this.createSearch(ACTIONS);
    }
    createSearch(searchMap) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const options = Object.assign(Object.assign({}, this.props.searchOptions), { keys: ['title', 'description'] });
            this.setState({
                fuzzy: yield (0, createFuzzySearch_1.createFuzzySearch)(searchMap || [], options),
            });
        });
    }
    render() {
        const { searchMap, query, isSuperuser, children } = this.props;
        let results = [];
        if (this.state.fuzzy) {
            const rawResults = this.state.fuzzy.search(query);
            results = rawResults
                .filter(({ item }) => !item.requiresSuperuser || isSuperuser)
                .map(value => {
                const { item } = value, rest = (0, tslib_1.__rest)(value, ["item"]);
                return Object.assign({ item: Object.assign(Object.assign({}, item), { sourceType: 'command', resultType: 'command' }) }, rest);
            });
        }
        return children({
            isLoading: searchMap === null,
            results,
        });
    }
}
exports.CommandSource = CommandSource;
CommandSource.defaultProps = {
    searchMap: [],
    searchOptions: {},
};
const CommandSourceWithFeature = (props) => (<access_1.default isSuperuser>
    {({ hasSuperuser }) => <CommandSource {...props} isSuperuser={hasSuperuser}/>}
  </access_1.default>);
exports.default = CommandSourceWithFeature;
//# sourceMappingURL=commandSource.jsx.map