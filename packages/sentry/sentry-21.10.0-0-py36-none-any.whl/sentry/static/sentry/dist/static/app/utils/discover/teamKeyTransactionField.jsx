Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const teamKeyTransaction_1 = (0, tslib_1.__importDefault)(require("app/components/performance/teamKeyTransaction"));
const TeamKeyTransactionManager = (0, tslib_1.__importStar)(require("app/components/performance/teamKeyTransactionsManager"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const utils_1 = require("app/utils");
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
class TitleStar extends react_1.Component {
    render() {
        var _a, _b;
        const _c = this.props, { isOpen, keyedTeams, initialValue } = _c, props = (0, tslib_1.__rest)(_c, ["isOpen", "keyedTeams", "initialValue"]);
        const keyedTeamsCount = (_b = (_a = keyedTeams === null || keyedTeams === void 0 ? void 0 : keyedTeams.length) !== null && _a !== void 0 ? _a : initialValue) !== null && _b !== void 0 ? _b : 0;
        const star = (<icons_1.IconStar color={keyedTeamsCount ? 'yellow300' : 'gray200'} isSolid={keyedTeamsCount > 0} data-test-id="team-key-transaction-column"/>);
        const button = <button_1.default {...props} icon={star} borderless size="zero"/>;
        if (!isOpen && (keyedTeams === null || keyedTeams === void 0 ? void 0 : keyedTeams.length)) {
            const teamSlugs = keyedTeams.map(({ slug }) => slug).join(', ');
            return <tooltip_1.default title={teamSlugs}>{button}</tooltip_1.default>;
        }
        else {
            return button;
        }
    }
}
function TeamKeyTransactionField(_a) {
    var { isKeyTransaction, counts, getKeyedTeams, project, transactionName } = _a, props = (0, tslib_1.__rest)(_a, ["isKeyTransaction", "counts", "getKeyedTeams", "project", "transactionName"]);
    const keyedTeams = getKeyedTeams(project.id, transactionName);
    return (<teamKeyTransaction_1.default counts={counts} keyedTeams={keyedTeams} title={TitleStar} project={project} transactionName={transactionName} initialValue={Number(isKeyTransaction)} {...props}/>);
}
function TeamKeyTransactionFieldWrapper(_a) {
    var { isKeyTransaction, projects, projectSlug, transactionName } = _a, props = (0, tslib_1.__rest)(_a, ["isKeyTransaction", "projects", "projectSlug", "transactionName"]);
    const project = projects.find(proj => proj.slug === projectSlug);
    // All these fields need to be defined in order to toggle a team key
    // transaction. Since they are not defined, just render a plain star
    // with no interactions.
    if (!(0, utils_1.defined)(project) || !(0, utils_1.defined)(transactionName)) {
        return (<TitleStar isOpen={false} disabled keyedTeams={null} initialValue={Number(isKeyTransaction)}/>);
    }
    return (<TeamKeyTransactionManager.Consumer>
      {results => (<TeamKeyTransactionField isKeyTransaction={isKeyTransaction} project={project} transactionName={transactionName} {...props} {...results}/>)}
    </TeamKeyTransactionManager.Consumer>);
}
exports.default = (0, withTeams_1.default)((0, withProjects_1.default)(TeamKeyTransactionFieldWrapper));
//# sourceMappingURL=teamKeyTransactionField.jsx.map