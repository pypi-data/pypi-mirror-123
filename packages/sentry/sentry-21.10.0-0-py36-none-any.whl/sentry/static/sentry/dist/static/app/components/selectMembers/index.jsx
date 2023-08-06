Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const memberListStore_1 = (0, tslib_1.__importDefault)(require("app/stores/memberListStore"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const getSearchKeyForUser = (user) => `${user.email && user.email.toLowerCase()} ${user.name && user.name.toLowerCase()}`;
/**
 * A component that allows you to select either members and/or teams
 */
class SelectMembers extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: false,
            inputValue: '',
            options: null,
            memberListLoading: !memberListStore_1.default.isLoaded(),
        };
        this.unlisteners = [
            memberListStore_1.default.listen(() => {
                this.setState({
                    memberListLoading: !memberListStore_1.default.isLoaded(),
                });
            }, undefined),
        ];
        this.renderUserBadge = (user) => (<idBadge_1.default avatarSize={24} user={user} hideEmail useLink={false}/>);
        this.createMentionableUser = (user) => ({
            value: user.id,
            label: this.renderUserBadge(user),
            searchKey: getSearchKeyForUser(user),
            actor: {
                type: 'user',
                id: user.id,
                name: user.name,
            },
        });
        this.createUnmentionableUser = ({ user }) => (Object.assign(Object.assign({}, this.createMentionableUser(user)), { disabled: true, label: (<DisabledLabel>
        <tooltip_1.default position="left" title={(0, locale_1.t)('%s is not a member of project', user.name || user.email)}>
          {this.renderUserBadge(user)}
        </tooltip_1.default>
      </DisabledLabel>) }));
        this.handleChange = newValue => {
            this.props.onChange(newValue);
        };
        this.handleInputChange = inputValue => {
            this.setState({ inputValue });
            if (this.props.onInputChange) {
                this.props.onInputChange(inputValue);
            }
        };
        this.queryMembers = (0, debounce_1.default)((query, cb) => {
            const { api, organization } = this.props;
            // Because this function is debounced, the component can potentially be
            // unmounted before this fires, in which case, `api` is null
            if (!api) {
                return null;
            }
            return api
                .requestPromise(`/organizations/${organization.slug}/members/`, {
                query: { query },
            })
                .then((data) => cb(null, data), err => cb(err));
        }, 250);
        this.handleLoadOptions = () => {
            const usersInProject = this.getMentionableUsers();
            const usersInProjectById = usersInProject.map(({ actor }) => actor.id);
            // Return a promise for `react-select`
            return new Promise((resolve, reject) => {
                this.queryMembers(this.state.inputValue, (err, result) => {
                    if (err) {
                        reject(err);
                    }
                    else {
                        resolve(result);
                    }
                });
            })
                .then(members => 
            // Be careful here as we actually want the `users` object, otherwise it means user
            // has not registered for sentry yet, but has been invited
            (members
                ? members
                    .filter(({ user }) => user && usersInProjectById.indexOf(user.id) === -1)
                    .map(this.createUnmentionableUser)
                : []))
                .then((members) => {
                const options = [...usersInProject, ...members];
                this.setState({ options });
                return options;
            });
        };
    }
    componentWillUnmount() {
        this.unlisteners.forEach(callIfFunction_1.callIfFunction);
    }
    getMentionableUsers() {
        return memberListStore_1.default.getAll().map(this.createMentionableUser);
    }
    render() {
        var _a;
        const { placeholder, styles } = this.props;
        // If memberList is still loading we need to disable a placeholder Select,
        // otherwise `react-select` will call `loadOptions` and prematurely load
        // options
        if (this.state.memberListLoading) {
            return <StyledSelectControl isDisabled placeholder={(0, locale_1.t)('Loading')}/>;
        }
        return (<StyledSelectControl filterOption={(option, filterText) => { var _a, _b; return ((_b = (_a = option === null || option === void 0 ? void 0 : option.data) === null || _a === void 0 ? void 0 : _a.searchKey) === null || _b === void 0 ? void 0 : _b.indexOf(filterText)) > -1; }} loadOptions={this.handleLoadOptions} isOptionDisabled={option => option.disabled} defaultOptions async isDisabled={this.props.disabled} cacheOptions={false} placeholder={placeholder} onInputChange={this.handleInputChange} onChange={this.handleChange} value={(_a = this.state.options) === null || _a === void 0 ? void 0 : _a.find(({ value }) => value === this.props.value)} styles={Object.assign(Object.assign({}, (styles !== null && styles !== void 0 ? styles : {})), { option: (provided, state) => (Object.assign(Object.assign({}, provided), { svg: {
                        color: state.isSelected && state.theme.white,
                    } })) })}/>);
    }
}
const DisabledLabel = (0, styled_1.default)('div') `
  display: flex;
  opacity: 0.5;
  overflow: hidden; /* Needed so that "Add to team" button can fit */
`;
const StyledSelectControl = (0, styled_1.default)(selectControl_1.default) `
  .Select-value {
    display: flex;
    align-items: center;
  }
  .Select-input {
    margin-left: 32px;
  }
`;
exports.default = (0, withApi_1.default)(SelectMembers);
//# sourceMappingURL=index.jsx.map