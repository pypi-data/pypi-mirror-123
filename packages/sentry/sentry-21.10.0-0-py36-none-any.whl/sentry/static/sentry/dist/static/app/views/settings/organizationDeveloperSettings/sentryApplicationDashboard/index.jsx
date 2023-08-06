Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const barChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/barChart"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const requestLog_1 = (0, tslib_1.__importDefault)(require("./requestLog"));
class SentryApplicationDashboard extends asyncView_1.default {
    getEndpoints() {
        const { appSlug } = this.props.params;
        // Default time range for now: 90 days ago to now
        const now = Math.floor(new Date().getTime() / 1000);
        const ninety_days_ago = 3600 * 24 * 90;
        return [
            [
                'stats',
                `/sentry-apps/${appSlug}/stats/`,
                { query: { since: now - ninety_days_ago, until: now } },
            ],
            [
                'interactions',
                `/sentry-apps/${appSlug}/interaction/`,
                { query: { since: now - ninety_days_ago, until: now } },
            ],
            ['app', `/sentry-apps/${appSlug}/`],
        ];
    }
    getTitle() {
        return (0, locale_1.t)('Integration Dashboard');
    }
    renderInstallData() {
        const { app, stats } = this.state;
        const { totalUninstalls, totalInstalls } = stats;
        return (<react_1.Fragment>
        <h5>{(0, locale_1.t)('Installation & Interaction Data')}</h5>
        <Row>
          {app.datePublished ? (<StatsSection>
              <StatsHeader>{(0, locale_1.t)('Date published')}</StatsHeader>
              <dateTime_1.default dateOnly date={app.datePublished}/>
            </StatsSection>) : null}
          <StatsSection>
            <StatsHeader>{(0, locale_1.t)('Total installs')}</StatsHeader>
            <p>{totalInstalls}</p>
          </StatsSection>
          <StatsSection>
            <StatsHeader>{(0, locale_1.t)('Total uninstalls')}</StatsHeader>
            <p>{totalUninstalls}</p>
          </StatsSection>
        </Row>
        {this.renderInstallCharts()}
      </react_1.Fragment>);
    }
    renderInstallCharts() {
        const { installStats, uninstallStats } = this.state.stats;
        const installSeries = {
            data: installStats.map(point => ({
                name: point[0] * 1000,
                value: point[1],
            })),
            seriesName: (0, locale_1.t)('installed'),
        };
        const uninstallSeries = {
            data: uninstallStats.map(point => ({
                name: point[0] * 1000,
                value: point[1],
            })),
            seriesName: (0, locale_1.t)('uninstalled'),
        };
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{(0, locale_1.t)('Installations/Uninstallations over Last 90 Days')}</panels_1.PanelHeader>
        <ChartWrapper>
          <barChart_1.default series={[installSeries, uninstallSeries]} height={150} stacked isGroupedByDate legend={{
                show: true,
                orient: 'horizontal',
                data: ['installed', 'uninstalled'],
                itemWidth: 15,
            }} yAxis={{ type: 'value', minInterval: 1, max: 'dataMax' }} xAxis={{ type: 'time' }} grid={{ left: (0, space_1.default)(4), right: (0, space_1.default)(4) }}/>
        </ChartWrapper>
      </panels_1.Panel>);
    }
    renderIntegrationViews() {
        const { views } = this.state.interactions;
        const { appSlug, orgId } = this.props.params;
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{(0, locale_1.t)('Integration Views')}</panels_1.PanelHeader>
        <panels_1.PanelBody>
          <InteractionsChart data={{ Views: views }}/>
        </panels_1.PanelBody>

        <panels_1.PanelFooter>
          <StyledFooter>
            {(0, locale_1.t)('Integration views are measured through views on the ')}
            <link_1.default to={`/sentry-apps/${appSlug}/external-install/`}>
              {(0, locale_1.t)('external installation page')}
            </link_1.default>
            {(0, locale_1.t)(' and views on the Learn More/Install modal on the ')}
            <link_1.default to={`/settings/${orgId}/integrations/`}>{(0, locale_1.t)('integrations page')}</link_1.default>
          </StyledFooter>
        </panels_1.PanelFooter>
      </panels_1.Panel>);
    }
    renderComponentInteractions() {
        const { componentInteractions } = this.state.interactions;
        const componentInteractionsDetails = {
            'stacktrace-link': (0, locale_1.t)('Each link click or context menu open counts as one interaction'),
            'issue-link': (0, locale_1.t)('Each open of the issue link modal counts as one interaction'),
        };
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{(0, locale_1.t)('Component Interactions')}</panels_1.PanelHeader>

        <panels_1.PanelBody>
          <InteractionsChart data={componentInteractions}/>
        </panels_1.PanelBody>

        <panels_1.PanelFooter>
          <StyledFooter>
            {Object.keys(componentInteractions).map((component, idx) => componentInteractionsDetails[component] && (<react_1.Fragment key={idx}>
                    <strong>{`${component}: `}</strong>
                    {componentInteractionsDetails[component]}
                    <br />
                  </react_1.Fragment>))}
          </StyledFooter>
        </panels_1.PanelFooter>
      </panels_1.Panel>);
    }
    renderBody() {
        const { app } = this.state;
        return (<div>
        <settingsPageHeader_1.default title={`${(0, locale_1.t)('Integration Dashboard')} - ${app.name}`}/>
        {app.status === 'published' && this.renderInstallData()}
        {app.status === 'published' && this.renderIntegrationViews()}
        {app.schema.elements && this.renderComponentInteractions()}
        <requestLog_1.default app={app}/>
      </div>);
    }
}
exports.default = SentryApplicationDashboard;
const InteractionsChart = ({ data }) => {
    const elementInteractionsSeries = Object.keys(data).map((key) => {
        const seriesData = data[key].map(point => ({
            value: point[1],
            name: point[0] * 1000,
        }));
        return {
            seriesName: key,
            data: seriesData,
        };
    });
    return (<ChartWrapper>
      <lineChart_1.default isGroupedByDate series={elementInteractionsSeries} grid={{ left: (0, space_1.default)(4), right: (0, space_1.default)(4) }} legend={{
            show: true,
            orient: 'horizontal',
            data: Object.keys(data),
        }}/>
    </ChartWrapper>);
};
const Row = (0, styled_1.default)('div') `
  display: flex;
`;
const StatsSection = (0, styled_1.default)('div') `
  margin-right: ${(0, space_1.default)(4)};
`;
const StatsHeader = (0, styled_1.default)('h6') `
  margin-bottom: ${(0, space_1.default)(1)};
  font-size: 12px;
  text-transform: uppercase;
  color: ${p => p.theme.subText};
`;
const StyledFooter = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(1.5)};
`;
const ChartWrapper = (0, styled_1.default)('div') `
  padding-top: ${(0, space_1.default)(3)};
`;
//# sourceMappingURL=index.jsx.map