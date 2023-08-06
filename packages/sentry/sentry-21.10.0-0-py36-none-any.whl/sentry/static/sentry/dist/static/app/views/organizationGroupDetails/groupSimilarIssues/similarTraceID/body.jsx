Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const moment_timezone_1 = (0, tslib_1.__importDefault)(require("moment-timezone"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const utils_1 = require("app/components/events/interfaces/spans/utils");
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const locale_1 = require("app/locale");
const discoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/discoverQuery"));
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const list_1 = (0, tslib_1.__importDefault)(require("./list"));
const Body = ({ traceID, organization, event, location }) => {
    if (!traceID) {
        return (<panels_1.Panel>
        <panels_1.PanelBody>
          <emptyStateWarning_1.default small withIcon={false}>
            {(0, locale_1.t)('This event has no trace context, therefore it was not possible to fetch similar issues by trace ID.')}
          </emptyStateWarning_1.default>
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
    const orgSlug = organization.slug;
    const orgFeatures = organization.features;
    const dateCreated = (0, moment_timezone_1.default)(event.dateCreated).valueOf() / 1000;
    const { start, end } = (0, utils_1.getTraceDateTimeRange)({ start: dateCreated, end: dateCreated });
    const eventView = eventView_1.default.fromSavedQuery({
        id: undefined,
        name: `Issues with Trace ID ${traceID}`,
        fields: ['issue.id'],
        orderby: '-timestamp',
        query: `trace:${traceID} !event.type:transaction !id:${event.id} `,
        projects: orgFeatures.includes('global-views')
            ? [globalSelectionHeader_1.ALL_ACCESS_PROJECTS]
            : [Number(event.projectID)],
        version: 2,
        start,
        end,
    });
    return (<discoverQuery_1.default eventView={eventView} location={location} orgSlug={orgSlug} limit={5}>
      {data => {
            var _a;
            if (data.isLoading) {
                return <loadingIndicator_1.default />;
            }
            const issues = ((_a = data === null || data === void 0 ? void 0 : data.tableData) === null || _a === void 0 ? void 0 : _a.data) || [];
            return (<list_1.default issues={issues} pageLinks={data.pageLinks} traceID={traceID} orgSlug={orgSlug} location={location} period={{ start, end }}/>);
        }}
    </discoverQuery_1.default>);
};
exports.default = Body;
//# sourceMappingURL=body.jsx.map