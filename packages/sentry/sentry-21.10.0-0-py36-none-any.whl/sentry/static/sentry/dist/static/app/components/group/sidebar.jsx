Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const isObject_1 = (0, tslib_1.__importDefault)(require("lodash/isObject"));
const keyBy_1 = (0, tslib_1.__importDefault)(require("lodash/keyBy"));
const pickBy_1 = (0, tslib_1.__importDefault)(require("lodash/pickBy"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const externalIssuesList_1 = (0, tslib_1.__importDefault)(require("app/components/group/externalIssuesList"));
const participants_1 = (0, tslib_1.__importDefault)(require("app/components/group/participants"));
const releaseStats_1 = (0, tslib_1.__importDefault)(require("app/components/group/releaseStats"));
const suggestedOwners_1 = (0, tslib_1.__importDefault)(require("app/components/group/suggestedOwners/suggestedOwners"));
const tagDistributionMeter_1 = (0, tslib_1.__importDefault)(require("app/components/group/tagDistributionMeter"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const sidebarSection_1 = (0, tslib_1.__importDefault)(require("./sidebarSection"));
class BaseGroupSidebar extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            participants: [],
            environments: this.props.environments,
        };
    }
    componentDidMount() {
        this.fetchAllEnvironmentsGroupData();
        this.fetchCurrentRelease();
        this.fetchParticipants();
        this.fetchTagData();
    }
    UNSAFE_componentWillReceiveProps(nextProps) {
        if (!(0, isEqual_1.default)(nextProps.environments, this.props.environments)) {
            this.setState({ environments: nextProps.environments }, this.fetchTagData);
        }
    }
    fetchAllEnvironmentsGroupData() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { group, api } = this.props;
            // Fetch group data for all environments since the one passed in props is filtered for the selected environment
            // The charts rely on having all environment data as well as the data for the selected env
            try {
                const query = { collapse: 'release' };
                const allEnvironmentsGroupData = yield api.requestPromise(`/issues/${group.id}/`, {
                    query,
                });
                // eslint-disable-next-line react/no-did-mount-set-state
                this.setState({ allEnvironmentsGroupData });
            }
            catch (_a) {
                // eslint-disable-next-line react/no-did-mount-set-state
                this.setState({ error: true });
            }
        });
    }
    fetchCurrentRelease() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { group, api } = this.props;
            try {
                const currentRelease = yield api.requestPromise(`/issues/${group.id}/current-release/`);
                this.setState({ currentRelease });
            }
            catch (_a) {
                this.setState({ error: true });
            }
        });
    }
    fetchParticipants() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { group, api } = this.props;
            try {
                const participants = yield api.requestPromise(`/issues/${group.id}/participants/`);
                this.setState({
                    participants,
                    error: false,
                });
                return participants;
            }
            catch (_a) {
                this.setState({
                    error: true,
                });
                return [];
            }
        });
    }
    fetchTagData() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, group } = this.props;
            try {
                // Fetch the top values for the current group's top tags.
                const data = yield api.requestPromise(`/issues/${group.id}/tags/`, {
                    query: (0, pickBy_1.default)({
                        key: group.tags.map(tag => tag.key),
                        environment: this.state.environments.map(env => env.name),
                    }),
                });
                this.setState({ tagsWithTopValues: (0, keyBy_1.default)(data, 'key') });
            }
            catch (_a) {
                this.setState({
                    tagsWithTopValues: {},
                    error: true,
                });
            }
        });
    }
    renderPluginIssue() {
        const issues = [];
        (this.props.group.pluginIssues || []).forEach(plugin => {
            const issue = plugin.issue;
            // # TODO(dcramer): remove plugin.title check in Sentry 8.22+
            if (issue) {
                issues.push(<React.Fragment key={plugin.slug}>
            <span>{`${plugin.shortName || plugin.name || plugin.title}: `}</span>
            <a href={issue.url}>{(0, isObject_1.default)(issue.label) ? issue.label.id : issue.label}</a>
          </React.Fragment>);
            }
        });
        if (!issues.length) {
            return null;
        }
        return (<sidebarSection_1.default title={(0, locale_1.t)('External Issues')}>
        <ExternalIssues>{issues}</ExternalIssues>
      </sidebarSection_1.default>);
    }
    renderParticipantData() {
        const { error, participants = [] } = this.state;
        if (error) {
            return (<loadingError_1.default message={(0, locale_1.t)('There was an error while trying to load participants.')}/>);
        }
        return participants.length !== 0 && <participants_1.default participants={participants}/>;
    }
    render() {
        const { className, event, group, organization, project, environments } = this.props;
        const { allEnvironmentsGroupData, currentRelease, tagsWithTopValues } = this.state;
        const projectId = project.slug;
        return (<div className={className}>
        {event && <suggestedOwners_1.default project={project} group={group} event={event}/>}

        <releaseStats_1.default organization={organization} project={project} environments={environments} allEnvironments={allEnvironmentsGroupData} group={group} currentRelease={currentRelease}/>

        {event && (<errorBoundary_1.default mini>
            <externalIssuesList_1.default project={project} group={group} event={event}/>
          </errorBoundary_1.default>)}

        {this.renderPluginIssue()}

        <sidebarSection_1.default title={<guideAnchor_1.default target="tags" position="bottom">
              {(0, locale_1.t)('Tags')}
            </guideAnchor_1.default>}>
          {!tagsWithTopValues ? (<TagPlaceholders>
              <placeholder_1.default height="40px"/>
              <placeholder_1.default height="40px"/>
              <placeholder_1.default height="40px"/>
              <placeholder_1.default height="40px"/>
            </TagPlaceholders>) : (group.tags.map(tag => {
                const tagWithTopValues = tagsWithTopValues[tag.key];
                const topValues = tagWithTopValues ? tagWithTopValues.topValues : [];
                const topValuesTotal = tagWithTopValues ? tagWithTopValues.totalValues : 0;
                return (<tagDistributionMeter_1.default key={tag.key} tag={tag.key} totalValues={topValuesTotal} topValues={topValues} name={tag.name} organization={organization} projectId={projectId} group={group}/>);
            }))}
          {group.tags.length === 0 && (<p data-test-id="no-tags">
              {environments.length
                    ? (0, locale_1.t)('No tags found in the selected environments')
                    : (0, locale_1.t)('No tags found')}
            </p>)}
        </sidebarSection_1.default>

        {this.renderParticipantData()}
      </div>);
    }
}
const TagPlaceholders = (0, styled_1.default)('div') `
  display: grid;
  gap: ${(0, space_1.default)(1)};
  grid-auto-flow: row;
`;
const ExternalIssues = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: auto max-content;
  gap: ${(0, space_1.default)(2)};
`;
const GroupSidebar = (0, styled_1.default)((0, withApi_1.default)(BaseGroupSidebar)) `
  font-size: ${p => p.theme.fontSizeMedium};
`;
exports.default = GroupSidebar;
//# sourceMappingURL=sidebar.jsx.map