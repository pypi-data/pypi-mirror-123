Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const assign_1 = (0, tslib_1.__importDefault)(require("lodash/assign"));
const memberListStore_1 = (0, tslib_1.__importDefault)(require("app/stores/memberListStore"));
const tagStore_1 = (0, tslib_1.__importDefault)(require("app/stores/tagStore"));
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
const uuidPattern = /[0-9a-f]{32}$/;
const getUsername = ({ isManaged, username, email }) => {
    // Users created via SAML receive unique UUID usernames. Use
    // their email in these cases, instead.
    if (username && uuidPattern.test(username)) {
        return email;
    }
    else {
        return !isManaged && username ? username : email;
    }
};
/**
 * HOC for getting tags and many useful issue attributes as 'tags' for use
 * in autocomplete selectors or condition builders.
 */
function withIssueTags(WrappedComponent) {
    class WithIssueTags extends React.Component {
        constructor(props, context) {
            super(props, context);
            this.unsubscribeMembers = memberListStore_1.default.listen((users) => {
                this.setState({ users });
                this.setAssigned();
            }, undefined);
            this.unsubscribeTeams = teamStore_1.default.listen(() => {
                this.setState({ teams: teamStore_1.default.getAll() });
                this.setAssigned();
            }, undefined);
            this.unsubscribeTags = tagStore_1.default.listen((storeTags) => {
                const tags = (0, assign_1.default)({}, storeTags, tagStore_1.default.getIssueAttributes(), tagStore_1.default.getBuiltInTags());
                this.setState({ tags });
                this.setAssigned();
            }, undefined);
            const tags = (0, assign_1.default)({}, tagStore_1.default.getAllTags(), tagStore_1.default.getIssueAttributes(), tagStore_1.default.getBuiltInTags());
            const users = memberListStore_1.default.getAll();
            const teams = teamStore_1.default.getAll();
            this.state = { tags, users, teams };
        }
        componentWillUnmount() {
            this.unsubscribeMembers();
            this.unsubscribeTeams();
            this.unsubscribeTags();
        }
        setAssigned() {
            const { tags, users, teams } = this.state;
            const usernames = users.map(getUsername);
            const teamnames = teams
                .filter(team => team.isMember)
                .map(team => `#${team.slug}`);
            const allAssigned = ['[me, none]', ...usernames.concat(teamnames)];
            allAssigned.unshift('me');
            usernames.unshift('me');
            this.setState({
                tags: Object.assign(Object.assign({}, tags), { assigned: Object.assign(Object.assign({}, tags.assigned), { values: allAssigned }), bookmarks: Object.assign(Object.assign({}, tags.bookmarks), { values: usernames }), assigned_or_suggested: Object.assign(Object.assign({}, tags.assigned_or_suggested), { values: allAssigned }) }),
            });
        }
        render() {
            const _a = this.props, { tags } = _a, props = (0, tslib_1.__rest)(_a, ["tags"]);
            return <WrappedComponent {...Object.assign({ tags: tags !== null && tags !== void 0 ? tags : this.state.tags }, props)}/>;
        }
    }
    WithIssueTags.displayName = `withIssueTags(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return WithIssueTags;
}
exports.default = withIssueTags;
//# sourceMappingURL=withIssueTags.jsx.map