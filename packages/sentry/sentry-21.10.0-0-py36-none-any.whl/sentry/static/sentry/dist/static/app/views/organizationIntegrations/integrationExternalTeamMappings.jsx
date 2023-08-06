Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const integrationExternalMappingForm_1 = (0, tslib_1.__importDefault)(require("app/components/integrationExternalMappingForm"));
const integrationExternalMappings_1 = (0, tslib_1.__importDefault)(require("app/components/integrationExternalMappings"));
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
class IntegrationExternalTeamMappings extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleDelete = (mapping) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            try {
                const { organization } = this.props;
                const { teams } = this.state;
                const team = teams.find(item => item.id === mapping.teamId);
                if (!team) {
                    throw new Error('Cannot find correct team slug.');
                }
                const endpoint = `/teams/${organization.slug}/${team.slug}/external-teams/${mapping.id}/`;
                yield this.api.requestPromise(endpoint, {
                    method: 'DELETE',
                });
                // remove config and update state
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Deletion successful'));
                this.fetchData();
            }
            catch (_a) {
                // no 4xx errors should happen on delete
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('An error occurred'));
            }
        });
        this.handleSubmitSuccess = () => {
            this.fetchData();
        };
        this.handleSubmit = (data, onSubmitSuccess, onSubmitError, _, model, mapping) => {
            // We need to dynamically set the endpoint bc it requires the slug of the selected team in the form.
            try {
                const { organization } = this.props;
                const { queryResults } = this.state;
                const team = queryResults.find(item => item.id === data.teamId);
                if (!team) {
                    throw new Error('Cannot find team slug.');
                }
                const baseEndpoint = `/teams/${organization.slug}/${team.slug}/external-teams/`;
                const apiEndpoint = mapping ? `${baseEndpoint}${mapping.id}/` : baseEndpoint;
                const apiMethod = mapping ? 'PUT' : 'POST';
                model.setFormOptions({
                    onSubmitSuccess,
                    onSubmitError,
                    apiEndpoint,
                    apiMethod,
                });
                model.saveForm();
            }
            catch (_a) {
                // no 4xx errors should happen on delete
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('An error occurred'));
            }
        };
        this.openModal = (mapping) => {
            const { organization, integration } = this.props;
            (0, modal_1.openModal)(({ Body, Header, closeModal }) => (<React.Fragment>
        <Header closeButton>{(0, locale_1.t)('Configure External Team Mapping')}</Header>
        <Body>
          <integrationExternalMappingForm_1.default organization={organization} integration={integration} onSubmitSuccess={() => {
                    this.handleSubmitSuccess();
                    closeModal();
                }} mapping={mapping} sentryNamesMapper={this.sentryNamesMapper} type="team" url={`/organizations/${organization.slug}/teams/`} onCancel={closeModal} onSubmit={(...args) => this.handleSubmit(...args, mapping)} onResults={results => this.setState({ queryResults: results })}/>
        </Body>
      </React.Fragment>));
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { teams: [], queryResults: [] });
    }
    getEndpoints() {
        const { organization } = this.props;
        return [
            [
                'teams',
                `/organizations/${organization.slug}/teams/`,
                { query: { query: 'hasExternalTeams:true' } },
            ],
        ];
    }
    get mappings() {
        const { integration } = this.props;
        const { teams } = this.state;
        const externalTeamMappings = teams.reduce((acc, team) => {
            const { externalTeams } = team;
            acc.push(...externalTeams
                .filter(externalTeam => externalTeam.provider === integration.provider.key)
                .map(externalTeam => (Object.assign(Object.assign({}, externalTeam), { sentryName: team.slug }))));
            return acc;
        }, []);
        return externalTeamMappings.sort((a, b) => parseInt(a.id, 10) - parseInt(b.id, 10));
    }
    sentryNamesMapper(teams) {
        return teams.map(({ id, slug }) => ({ id, name: slug }));
    }
    renderBody() {
        const { integration } = this.props;
        return (<integrationExternalMappings_1.default integration={integration} type="team" mappings={this.mappings} onCreateOrEdit={this.openModal} onDelete={this.handleDelete}/>);
    }
}
exports.default = (0, withOrganization_1.default)(IntegrationExternalTeamMappings);
//# sourceMappingURL=integrationExternalTeamMappings.jsx.map