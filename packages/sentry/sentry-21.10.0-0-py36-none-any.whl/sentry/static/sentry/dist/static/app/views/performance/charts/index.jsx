Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const eventsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsRequest"));
const loadingPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/loadingPanel"));
const styles_1 = require("app/components/charts/styles");
const utils_1 = require("app/components/charts/utils");
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const icons_1 = require("app/icons");
const dates_1 = require("app/utils/dates");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const data_1 = require("../data");
const styles_2 = require("../styles");
const chart_1 = (0, tslib_1.__importDefault)(require("./chart"));
const footer_1 = (0, tslib_1.__importDefault)(require("./footer"));
class Container extends react_1.Component {
    getChartParameters() {
        const { location, organization } = this.props;
        const options = (0, data_1.getAxisOptions)(organization);
        const left = options.find(opt => opt.value === location.query.left) || options[0];
        const right = options.find(opt => opt.value === location.query.right) || options[1];
        return [left, right];
    }
    render() {
        const { api, organization, location, eventView, router } = this.props;
        // construct request parameters for fetching chart data
        const globalSelection = eventView.getGlobalSelection();
        const start = globalSelection.datetime.start
            ? (0, dates_1.getUtcToLocalDateObject)(globalSelection.datetime.start)
            : null;
        const end = globalSelection.datetime.end
            ? (0, dates_1.getUtcToLocalDateObject)(globalSelection.datetime.end)
            : null;
        const { utc } = (0, getParams_1.getParams)(location.query);
        const axisOptions = this.getChartParameters();
        const apiPayload = eventView.getEventsAPIPayload(location);
        return (<panels_1.Panel>
        <eventsRequest_1.default organization={organization} api={api} period={globalSelection.datetime.period} project={globalSelection.projects} environment={globalSelection.environments} team={apiPayload.team} start={start} end={end} interval={(0, utils_1.getInterval)({
                start,
                end,
                period: globalSelection.datetime.period,
            }, 'high')} showLoading={false} query={apiPayload.query} includePrevious={false} yAxis={axisOptions.map(opt => opt.value)} partial>
          {({ loading, reloading, errored, results }) => {
                if (errored) {
                    return (<styles_2.ErrorPanel>
                  <icons_1.IconWarning color="gray300" size="lg"/>
                </styles_2.ErrorPanel>);
                }
                return (<react_1.Fragment>
                <styles_2.DoubleHeaderContainer>
                  {axisOptions.map((option, i) => (<div key={`${option.label}:${i}`}>
                      <styles_1.HeaderTitle>
                        {option.label}
                        <questionTooltip_1.default position="top" size="sm" title={option.tooltip}/>
                      </styles_1.HeaderTitle>
                    </div>))}
                </styles_2.DoubleHeaderContainer>
                {results ? ((0, getDynamicText_1.default)({
                        value: (<chart_1.default data={results} loading={loading || reloading} router={router} statsPeriod={globalSelection.datetime.period} start={start} end={end} utc={utc === 'true'}/>),
                        fixed: <placeholder_1.default height="200px" testId="skeleton-ui"/>,
                    })) : (<loadingPanel_1.default data-test-id="events-request-loading"/>)}
              </react_1.Fragment>);
            }}
        </eventsRequest_1.default>
        <footer_1.default api={api} leftAxis={axisOptions[0].value} rightAxis={axisOptions[1].value} organization={organization} eventView={eventView} location={location}/>
      </panels_1.Panel>);
    }
}
exports.default = (0, withApi_1.default)(Container);
//# sourceMappingURL=index.jsx.map