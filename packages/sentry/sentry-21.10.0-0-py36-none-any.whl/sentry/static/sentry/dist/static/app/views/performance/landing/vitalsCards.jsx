Object.defineProperty(exports, "__esModule", { value: true });
exports.VitalBar = exports.MobileCards = exports.BackendCards = exports.FrontendCards = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const card_1 = (0, tslib_1.__importDefault)(require("app/components/card"));
const eventsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsRequest"));
const styles_1 = require("app/components/charts/styles");
const utils_1 = require("app/components/charts/utils");
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const sparklines_1 = (0, tslib_1.__importDefault)(require("app/components/sparklines"));
const line_1 = (0, tslib_1.__importDefault)(require("app/components/sparklines/line"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_2 = require("app/utils");
const dates_1 = require("app/utils/dates");
const discoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/discoverQuery"));
const fields_1 = require("app/utils/discover/fields");
const constants_1 = require("app/utils/performance/vitals/constants");
const vitalsCardsDiscoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/vitals/vitalsCardsDiscoverQuery"));
const queryString_1 = require("app/utils/queryString");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const colorBar_1 = (0, tslib_1.__importDefault)(require("../vitalDetail/colorBar"));
const utils_3 = require("../vitalDetail/utils");
const vitalPercents_1 = (0, tslib_1.__importDefault)(require("../vitalDetail/vitalPercents"));
const utils_4 = require("./utils");
function FrontendCards(props) {
    const { eventView, location, organization, projects, frontendOnly = false } = props;
    if (frontendOnly) {
        const defaultDisplay = (0, utils_4.getDefaultDisplayFieldForPlatform)(projects, eventView);
        const isFrontend = defaultDisplay === utils_4.LandingDisplayField.FRONTEND_PAGELOAD;
        if (!isFrontend) {
            return null;
        }
    }
    const vitals = [fields_1.WebVital.FCP, fields_1.WebVital.LCP, fields_1.WebVital.FID, fields_1.WebVital.CLS];
    return (<vitalsCardsDiscoverQuery_1.default eventView={eventView} location={location} orgSlug={organization.slug} vitals={vitals}>
      {({ isLoading, vitalsData }) => {
            return (<VitalsContainer>
            {vitals.map(vital => {
                    var _a, _b, _c;
                    const target = (0, utils_3.vitalDetailRouteWithQuery)({
                        orgSlug: organization.slug,
                        query: eventView.generateQueryStringObject(),
                        vitalName: vital,
                        projectID: (0, queryString_1.decodeList)(location.query.project),
                    });
                    const value = isLoading
                        ? '\u2014'
                        : getP75((_a = vitalsData === null || vitalsData === void 0 ? void 0 : vitalsData[vital]) !== null && _a !== void 0 ? _a : null, vital);
                    const chart = (<VitalBarContainer>
                  <VitalBar isLoading={isLoading} vital={vital} data={vitalsData}/>
                </VitalBarContainer>);
                    return (<link_1.default key={vital} to={target} data-test-id={`vitals-linked-card-${utils_3.vitalAbbreviations[vital]}`}>
                  <VitalCard title={(_b = utils_3.vitalMap[vital]) !== null && _b !== void 0 ? _b : ''} tooltip={(_c = constants_1.WEB_VITAL_DETAILS[vital].description) !== null && _c !== void 0 ? _c : ''} value={isLoading ? '\u2014' : value} chart={chart} minHeight={150}/>
                </link_1.default>);
                })}
          </VitalsContainer>);
        }}
    </vitalsCardsDiscoverQuery_1.default>);
}
exports.FrontendCards = FrontendCards;
const VitalBarContainer = (0, styled_1.default)('div') `
  margin-top: ${(0, space_1.default)(1.5)};
`;
function GenericCards(props) {
    const api = (0, useApi_1.default)();
    const { eventView: baseEventView, location, organization, functions } = props;
    const { query } = location;
    const eventView = baseEventView.withColumns(functions);
    // construct request parameters for fetching chart data
    const globalSelection = eventView.getGlobalSelection();
    const start = globalSelection.datetime.start
        ? (0, dates_1.getUtcToLocalDateObject)(globalSelection.datetime.start)
        : undefined;
    const end = globalSelection.datetime.end
        ? (0, dates_1.getUtcToLocalDateObject)(globalSelection.datetime.end)
        : undefined;
    const interval = typeof query.sparkInterval === 'string'
        ? query.sparkInterval
        : (0, utils_1.getInterval)({
            start: start || null,
            end: end || null,
            period: globalSelection.datetime.period,
        }, 'low');
    const apiPayload = eventView.getEventsAPIPayload(location);
    return (<discoverQuery_1.default location={location} eventView={eventView} orgSlug={organization.slug} limit={1} referrer="api.performance.vitals-cards">
      {({ isLoading: isSummaryLoading, tableData }) => (<eventsRequest_1.default api={api} organization={organization} period={globalSelection.datetime.period} project={globalSelection.projects} environment={globalSelection.environments} team={apiPayload.team} start={start} end={end} interval={interval} query={apiPayload.query} includePrevious={false} yAxis={eventView.getFields()} partial>
          {({ results }) => {
                const series = results === null || results === void 0 ? void 0 : results.reduce((allSeries, oneSeries) => {
                    allSeries[oneSeries.seriesName] = oneSeries.data.map(item => item.value);
                    return allSeries;
                }, {});
                const details = (0, utils_4.vitalCardDetails)(organization);
                return (<VitalsContainer>
                {functions.map(func => {
                        var _a, _b;
                        let fieldName = (0, fields_1.generateFieldAsString)(func);
                        if (fieldName.includes('apdex')) {
                            // Replace apdex with explicit thresholds with a generic one for lookup
                            fieldName = 'apdex()';
                        }
                        const cardDetail = details[fieldName];
                        if (!cardDetail) {
                            Sentry.captureMessage(`Missing field '${fieldName}' in vital cards.`);
                            return null;
                        }
                        const { title, tooltip, formatter } = cardDetail;
                        const alias = (0, fields_1.getAggregateAlias)(fieldName);
                        const rawValue = (_b = (_a = tableData === null || tableData === void 0 ? void 0 : tableData.data) === null || _a === void 0 ? void 0 : _a[0]) === null || _b === void 0 ? void 0 : _b[alias];
                        const data = series === null || series === void 0 ? void 0 : series[fieldName];
                        const value = isSummaryLoading || !(0, utils_2.defined)(rawValue)
                            ? '\u2014'
                            : formatter(rawValue);
                        const chart = <SparklineChart data={data}/>;
                        return (<VitalCard key={fieldName} title={title} tooltip={tooltip} value={value} chart={chart} horizontal minHeight={96} isNotInteractive/>);
                    })}
              </VitalsContainer>);
            }}
        </eventsRequest_1.default>)}
    </discoverQuery_1.default>);
}
function _BackendCards(props) {
    const functions = [
        {
            kind: 'function',
            function: ['p75', 'transaction.duration', undefined, undefined],
        },
        { kind: 'function', function: ['tpm', '', undefined, undefined] },
        { kind: 'function', function: ['failure_rate', '', undefined, undefined] },
        {
            kind: 'function',
            function: ['apdex', '', undefined, undefined],
        },
    ];
    return <GenericCards {...props} functions={functions}/>;
}
exports.BackendCards = _BackendCards;
function _MobileCards(props) {
    const functions = [
        {
            kind: 'function',
            function: ['p75', 'measurements.app_start_cold', undefined, undefined],
        },
        {
            kind: 'function',
            function: ['p75', 'measurements.app_start_warm', undefined, undefined],
        },
    ];
    if (props.showStallPercentage) {
        functions.push({
            kind: 'function',
            function: ['p75', 'measurements.stall_percentage', undefined, undefined],
        });
    }
    else {
        // TODO(tonyx): add these by default once the SDKs are ready
        functions.push({
            kind: 'function',
            function: ['p75', 'measurements.frames_slow_rate', undefined, undefined],
        });
        functions.push({
            kind: 'function',
            function: ['p75', 'measurements.frames_frozen_rate', undefined, undefined],
        });
    }
    return <GenericCards {...props} functions={functions}/>;
}
exports.MobileCards = _MobileCards;
function SparklineChart(props) {
    const { data } = props;
    const width = 150;
    const height = 24;
    const lineColor = theme_1.default.charts.getColorPalette(1)[0];
    return (<SparklineContainer data-test-id="sparkline" width={width} height={height}>
      <sparklines_1.default data={data} width={width} height={height}>
        <line_1.default style={{ stroke: lineColor, fill: 'none', strokeWidth: 3 }}/>
      </sparklines_1.default>
    </SparklineContainer>);
}
const SparklineContainer = (0, styled_1.default)('div') `
  flex-grow: 4;
  max-height: ${p => p.height}px;
  max-width: ${p => p.width}px;
  margin: ${(0, space_1.default)(1)} ${(0, space_1.default)(0)} ${(0, space_1.default)(0.5)} ${(0, space_1.default)(3)};
`;
const VitalsContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr;
  grid-column-gap: ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
`;
function VitalBar(props) {
    var _a;
    const { isLoading, data, vital, value, showBar = true, showStates = false, showDurationDetail = false, showVitalPercentNames = false, } = props;
    if (isLoading) {
        return showStates ? <placeholder_1.default height="48px"/> : null;
    }
    const emptyState = showStates ? (<EmptyVitalBar small>{(0, locale_1.t)('No vitals found')}</EmptyVitalBar>) : null;
    if (!data) {
        return emptyState;
    }
    const counts = {
        poor: 0,
        meh: 0,
        good: 0,
        total: 0,
    };
    const vitals = Array.isArray(vital) ? vital : [vital];
    vitals.forEach(vitalName => {
        var _a;
        const c = (_a = data === null || data === void 0 ? void 0 : data[vitalName]) !== null && _a !== void 0 ? _a : {};
        Object.keys(counts).forEach(countKey => (counts[countKey] += c[countKey]));
    });
    if (!counts.total) {
        return emptyState;
    }
    const p75 = Array.isArray(vital)
        ? null
        : value !== null && value !== void 0 ? value : getP75((_a = data === null || data === void 0 ? void 0 : data[vital]) !== null && _a !== void 0 ? _a : null, vital);
    const percents = getPercentsFromCounts(counts);
    const colorStops = getColorStopsFromPercents(percents);
    return (<React.Fragment>
      {showBar && <colorBar_1.default colorStops={colorStops}/>}
      <BarDetail>
        {showDurationDetail && p75 && (<div data-test-id="vital-bar-p75">
            {(0, locale_1.t)('The p75 for all transactions is ')}
            <strong>{p75}</strong>
          </div>)}
        <vitalPercents_1.default vital={vital} percents={percents} showVitalPercentNames={showVitalPercentNames}/>
      </BarDetail>
    </React.Fragment>);
}
exports.VitalBar = VitalBar;
const EmptyVitalBar = (0, styled_1.default)(emptyStateWarning_1.default) `
  height: 48px;
  padding: ${(0, space_1.default)(1.5)} 15%;
`;
function VitalCard(props) {
    const { chart, minHeight, horizontal, title, tooltip, value, isNotInteractive } = props;
    return (<StyledCard interactive={!isNotInteractive} minHeight={minHeight}>
      <styles_1.HeaderTitle>
        <OverflowEllipsis>{(0, locale_1.t)(title)}</OverflowEllipsis>
        <questionTooltip_1.default size="sm" position="top" title={tooltip}/>
      </styles_1.HeaderTitle>
      <CardContent horizontal={horizontal}>
        <CardValue>{value}</CardValue>
        {chart}
      </CardContent>
    </StyledCard>);
}
const CardContent = (0, styled_1.default)('div') `
  width: 100%;
  display: flex;
  flex-direction: ${p => (p.horizontal ? 'row' : 'column')};
  justify-content: space-between;
`;
const StyledCard = (0, styled_1.default)(card_1.default) `
  color: ${p => p.theme.textColor};
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(3)};
  align-items: flex-start;
  margin-bottom: ${(0, space_1.default)(2)};
  ${p => p.minHeight && `min-height: ${p.minHeight}px`};
`;
function getP75(data, vitalName) {
    var _a;
    const p75 = (_a = data === null || data === void 0 ? void 0 : data.p75) !== null && _a !== void 0 ? _a : null;
    if (p75 === null) {
        return '\u2014';
    }
    else {
        return vitalName === fields_1.WebVital.CLS ? p75.toFixed(2) : `${p75.toFixed(0)}ms`;
    }
}
function getPercentsFromCounts({ poor, meh, good, total }) {
    const poorPercent = poor / total;
    const mehPercent = meh / total;
    const goodPercent = good / total;
    const percents = [
        {
            vitalState: utils_3.VitalState.GOOD,
            percent: goodPercent,
        },
        {
            vitalState: utils_3.VitalState.MEH,
            percent: mehPercent,
        },
        {
            vitalState: utils_3.VitalState.POOR,
            percent: poorPercent,
        },
    ];
    return percents;
}
function getColorStopsFromPercents(percents) {
    return percents.map(({ percent, vitalState }) => ({
        percent,
        color: utils_3.vitalStateColors[vitalState],
    }));
}
const BarDetail = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    display: flex;
    justify-content: space-between;
  }
`;
const CardValue = (0, styled_1.default)('div') `
  font-size: 32px;
  margin-top: ${(0, space_1.default)(1)};
`;
const OverflowEllipsis = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default};
`;
//# sourceMappingURL=vitalsCards.jsx.map