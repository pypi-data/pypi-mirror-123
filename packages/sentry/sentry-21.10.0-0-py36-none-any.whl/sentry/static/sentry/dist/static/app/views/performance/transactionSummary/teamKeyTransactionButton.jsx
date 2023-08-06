Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const teamKeyTransaction_1 = (0, tslib_1.__importDefault)(require("app/components/performance/teamKeyTransaction"));
const TeamKeyTransactionManager = (0, tslib_1.__importStar)(require("app/components/performance/teamKeyTransactionsManager"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const isActiveSuperuser_1 = require("app/utils/isActiveSuperuser");
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
/**
 * This can't be a function component because `TeamKeyTransaction` uses
 * `DropdownControl` which in turn uses passes a ref to this component.
 */
class TitleButton extends react_1.Component {
    render() {
        var _a;
        const _b = this.props, { isOpen, keyedTeams } = _b, props = (0, tslib_1.__rest)(_b, ["isOpen", "keyedTeams"]);
        const keyedTeamsCount = (_a = keyedTeams === null || keyedTeams === void 0 ? void 0 : keyedTeams.length) !== null && _a !== void 0 ? _a : 0;
        const button = (<button_1.default {...props} icon={keyedTeamsCount ? <icons_1.IconStar color="yellow300" isSolid/> : <icons_1.IconStar />}>
        {keyedTeamsCount
                ? (0, locale_1.tn)('Starred for Team', 'Starred for Teams', keyedTeamsCount)
                : (0, locale_1.t)('Star for Team')}
      </button_1.default>);
        if (!isOpen && (keyedTeams === null || keyedTeams === void 0 ? void 0 : keyedTeams.length)) {
            const teamSlugs = keyedTeams.map(({ slug }) => slug).join(', ');
            return <tooltip_1.default title={teamSlugs}>{button}</tooltip_1.default>;
        }
        else {
            return button;
        }
    }
}
function TeamKeyTransactionButton(_a) {
    var { counts, getKeyedTeams, project, transactionName } = _a, props = (0, tslib_1.__rest)(_a, ["counts", "getKeyedTeams", "project", "transactionName"]);
    const keyedTeams = getKeyedTeams(project.id, transactionName);
    return (<teamKeyTransaction_1.default counts={counts} keyedTeams={keyedTeams} title={TitleButton} project={project} transactionName={transactionName} {...props}/>);
}
function TeamKeyTransactionButtonWrapper(_a) {
    var { eventView, organization, teams, projects } = _a, props = (0, tslib_1.__rest)(_a, ["eventView", "organization", "teams", "projects"]);
    if (eventView.project.length !== 1) {
        return <TitleButton isOpen={false} disabled keyedTeams={null}/>;
    }
    const projectId = String(eventView.project[0]);
    const project = projects.find(proj => proj.id === projectId);
    if (!(0, utils_1.defined)(project)) {
        return <TitleButton isOpen={false} disabled keyedTeams={null}/>;
    }
    const isSuperuser = (0, isActiveSuperuser_1.isActiveSuperuser)();
    const userTeams = teams.filter(({ isMember }) => isMember || isSuperuser);
    return (<TeamKeyTransactionManager.Provider organization={organization} teams={userTeams} selectedTeams={['myteams']} selectedProjects={[String(projectId)]}>
      <TeamKeyTransactionManager.Consumer>
        {results => (<TeamKeyTransactionButton organization={organization} project={project} {...props} {...results}/>)}
      </TeamKeyTransactionManager.Consumer>
    </TeamKeyTransactionManager.Provider>);
}
exports.default = (0, withTeams_1.default)((0, withProjects_1.default)(TeamKeyTransactionButtonWrapper));
//# sourceMappingURL=teamKeyTransactionButton.jsx.map