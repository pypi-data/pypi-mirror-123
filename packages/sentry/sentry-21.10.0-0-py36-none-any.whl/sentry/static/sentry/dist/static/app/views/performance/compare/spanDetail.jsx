Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const spanDetail_1 = require("app/components/events/interfaces/spans/spanDetail");
const types_1 = require("app/components/events/interfaces/spans/types");
const utils_1 = require("app/components/performance/waterfall/utils");
const pill_1 = (0, tslib_1.__importDefault)(require("app/components/pill"));
const pills_1 = (0, tslib_1.__importDefault)(require("app/components/pills"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const spanDetailContent_1 = (0, tslib_1.__importDefault)(require("./spanDetailContent"));
const styles_1 = require("./styles");
const utils_2 = require("./utils");
const getDurationDisplay = (width) => {
    if (!width) {
        return 'right';
    }
    switch (width.type) {
        case 'WIDTH_PIXEL': {
            return 'right';
        }
        case 'WIDTH_PERCENTAGE': {
            const spaceNeeded = 0.3;
            if (width.width < 1 - spaceNeeded) {
                return 'right';
            }
            return 'inset';
        }
        default: {
            const _exhaustiveCheck = width;
            return _exhaustiveCheck;
        }
    }
};
class SpanDetail extends React.Component {
    renderContent() {
        const { span, bounds } = this.props;
        switch (span.comparisonResult) {
            case 'matched': {
                return (<MatchedSpanDetailsContent baselineSpan={span.baselineSpan} regressionSpan={span.regressionSpan} bounds={bounds}/>);
            }
            case 'regression': {
                return <spanDetailContent_1.default span={span.regressionSpan}/>;
            }
            case 'baseline': {
                return <spanDetailContent_1.default span={span.baselineSpan}/>;
            }
            default: {
                const _exhaustiveCheck = span;
                return _exhaustiveCheck;
            }
        }
    }
    render() {
        return (<spanDetail_1.SpanDetailContainer onClick={event => {
                // prevent toggling the span detail
                event.stopPropagation();
            }}>
        {this.renderContent()}
      </spanDetail_1.SpanDetailContainer>);
    }
}
const MatchedSpanDetailsContent = (props) => {
    var _a, _b;
    const { baselineSpan, regressionSpan, bounds } = props;
    const dataKeys = new Set([
        ...Object.keys((_a = baselineSpan === null || baselineSpan === void 0 ? void 0 : baselineSpan.data) !== null && _a !== void 0 ? _a : {}),
        ...Object.keys((_b = regressionSpan === null || regressionSpan === void 0 ? void 0 : regressionSpan.data) !== null && _b !== void 0 ? _b : {}),
    ]);
    const unknownKeys = new Set([
        ...Object.keys(baselineSpan).filter(key => {
            return !types_1.rawSpanKeys.has(key);
        }),
        ...Object.keys(regressionSpan).filter(key => {
            return !types_1.rawSpanKeys.has(key);
        }),
    ]);
    return (<div>
      <SpanBars bounds={bounds} baselineSpan={baselineSpan} regressionSpan={regressionSpan}/>
      <Row baselineTitle={(0, locale_1.t)('Baseline Span ID')} regressionTitle={(0, locale_1.t)("This Event's Span ID")} renderBaselineContent={() => baselineSpan.span_id} renderRegressionContent={() => regressionSpan.span_id}/>
      <Row title={(0, locale_1.t)('Parent Span ID')} renderBaselineContent={() => baselineSpan.parent_span_id || ''} renderRegressionContent={() => regressionSpan.parent_span_id || ''}/>
      <Row title={(0, locale_1.t)('Trace ID')} renderBaselineContent={() => baselineSpan.trace_id} renderRegressionContent={() => regressionSpan.trace_id}/>
      <Row title={(0, locale_1.t)('Description')} renderBaselineContent={() => { var _a; return (_a = baselineSpan.description) !== null && _a !== void 0 ? _a : ''; }} renderRegressionContent={() => { var _a; return (_a = regressionSpan.description) !== null && _a !== void 0 ? _a : ''; }}/>
      <Row title={(0, locale_1.t)('Start Date')} renderBaselineContent={() => (0, getDynamicText_1.default)({
            fixed: 'Mar 16, 2020 9:10:12 AM UTC',
            value: (<React.Fragment>
                <dateTime_1.default date={baselineSpan.start_timestamp * 1000}/>
                {` (${baselineSpan.start_timestamp})`}
              </React.Fragment>),
        })} renderRegressionContent={() => (0, getDynamicText_1.default)({
            fixed: 'Mar 16, 2020 9:10:12 AM UTC',
            value: (<React.Fragment>
                <dateTime_1.default date={regressionSpan.start_timestamp * 1000}/>
                {` (${baselineSpan.start_timestamp})`}
              </React.Fragment>),
        })}/>
      <Row title={(0, locale_1.t)('End Date')} renderBaselineContent={() => (0, getDynamicText_1.default)({
            fixed: 'Mar 16, 2020 9:10:12 AM UTC',
            value: (<React.Fragment>
                <dateTime_1.default date={baselineSpan.timestamp * 1000}/>
                {` (${baselineSpan.timestamp})`}
              </React.Fragment>),
        })} renderRegressionContent={() => (0, getDynamicText_1.default)({
            fixed: 'Mar 16, 2020 9:10:12 AM UTC',
            value: (<React.Fragment>
                <dateTime_1.default date={regressionSpan.timestamp * 1000}/>
                {` (${regressionSpan.timestamp})`}
              </React.Fragment>),
        })}/>
      <Row title={(0, locale_1.t)('Duration')} renderBaselineContent={() => {
            const startTimestamp = baselineSpan.start_timestamp;
            const endTimestamp = baselineSpan.timestamp;
            const duration = (endTimestamp - startTimestamp) * 1000;
            return `${duration.toFixed(3)}ms`;
        }} renderRegressionContent={() => {
            const startTimestamp = regressionSpan.start_timestamp;
            const endTimestamp = regressionSpan.timestamp;
            const duration = (endTimestamp - startTimestamp) * 1000;
            return `${duration.toFixed(3)}ms`;
        }}/>
      <Row title={(0, locale_1.t)('Operation')} renderBaselineContent={() => baselineSpan.op || ''} renderRegressionContent={() => regressionSpan.op || ''}/>
      <Row title={(0, locale_1.t)('Same Process as Parent')} renderBaselineContent={() => String(!!baselineSpan.same_process_as_parent)} renderRegressionContent={() => String(!!regressionSpan.same_process_as_parent)}/>
      <Tags baselineSpan={baselineSpan} regressionSpan={regressionSpan}/>
      {Array.from(dataKeys).map((dataTitle) => (<Row key={dataTitle} title={dataTitle} renderBaselineContent={() => {
                var _a;
                const data = (_a = baselineSpan === null || baselineSpan === void 0 ? void 0 : baselineSpan.data) !== null && _a !== void 0 ? _a : {};
                const value = data[dataTitle];
                return JSON.stringify(value, null, 4) || '';
            }} renderRegressionContent={() => {
                var _a;
                const data = (_a = regressionSpan === null || regressionSpan === void 0 ? void 0 : regressionSpan.data) !== null && _a !== void 0 ? _a : {};
                const value = data[dataTitle];
                return JSON.stringify(value, null, 4) || '';
            }}/>))}
      {Array.from(unknownKeys).map(key => (<Row key={key} title={key} renderBaselineContent={() => {
                return JSON.stringify(baselineSpan[key], null, 4) || '';
            }} renderRegressionContent={() => {
                return JSON.stringify(regressionSpan[key], null, 4) || '';
            }}/>))}
    </div>);
};
const RowSplitter = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: row;

  > * + * {
    border-left: 1px solid ${p => p.theme.border};
  }
`;
const SpanBarContainer = (0, styled_1.default)('div') `
  position: relative;
  height: 16px;
  margin-top: ${(0, space_1.default)(3)};
  margin-bottom: ${(0, space_1.default)(2)};
`;
const SpanBars = (props) => {
    const { bounds, baselineSpan, regressionSpan } = props;
    const baselineDurationDisplay = getDurationDisplay(bounds.baseline);
    const regressionDurationDisplay = getDurationDisplay(bounds.regression);
    return (<RowSplitter>
      <RowContainer>
        <SpanBarContainer>
          <styles_1.SpanBarRectangle style={{
            backgroundColor: theme_1.default.gray500,
            width: (0, utils_2.generateCSSWidth)(bounds.baseline),
            position: 'absolute',
            height: '16px',
        }}>
            <DurationPill durationDisplay={baselineDurationDisplay} fontColors={{ right: theme_1.default.gray500, inset: theme_1.default.white }}>
              {(0, utils_1.getHumanDuration)((0, utils_2.getSpanDuration)(baselineSpan))}
            </DurationPill>
          </styles_1.SpanBarRectangle>
        </SpanBarContainer>
      </RowContainer>
      <RowContainer>
        <SpanBarContainer>
          <styles_1.SpanBarRectangle style={{
            backgroundColor: theme_1.default.purple200,
            width: (0, utils_2.generateCSSWidth)(bounds.regression),
            position: 'absolute',
            height: '16px',
        }}>
            <DurationPill durationDisplay={regressionDurationDisplay} fontColors={{ right: theme_1.default.gray500, inset: theme_1.default.gray500 }}>
              {(0, utils_1.getHumanDuration)((0, utils_2.getSpanDuration)(regressionSpan))}
            </DurationPill>
          </styles_1.SpanBarRectangle>
        </SpanBarContainer>
      </RowContainer>
    </RowSplitter>);
};
const Row = (props) => {
    var _a, _b;
    const { title, baselineTitle, regressionTitle } = props;
    const baselineContent = props.renderBaselineContent();
    const regressionContent = props.renderRegressionContent();
    if (!baselineContent && !regressionContent) {
        return null;
    }
    return (<RowSplitter>
      <RowCell title={(_a = baselineTitle !== null && baselineTitle !== void 0 ? baselineTitle : title) !== null && _a !== void 0 ? _a : ''}>{baselineContent}</RowCell>
      <RowCell title={(_b = regressionTitle !== null && regressionTitle !== void 0 ? regressionTitle : title) !== null && _b !== void 0 ? _b : ''}>{regressionContent}</RowCell>
    </RowSplitter>);
};
const RowContainer = (0, styled_1.default)('div') `
  width: 50%;
  min-width: 50%;
  max-width: 50%;
  flex-basis: 50%;

  padding-left: ${(0, space_1.default)(2)};
  padding-right: ${(0, space_1.default)(2)};
`;
const RowTitle = (0, styled_1.default)('div') `
  font-size: 13px;
  font-weight: 600;
`;
const RowCell = ({ title, children }) => {
    return (<RowContainer>
      <RowTitle>{title}</RowTitle>
      <div>
        <pre className="val" style={{ marginBottom: (0, space_1.default)(1) }}>
          <span className="val-string">{children}</span>
        </pre>
      </div>
    </RowContainer>);
};
const getTags = (span) => {
    const tags = span === null || span === void 0 ? void 0 : span.tags;
    if (!tags) {
        return undefined;
    }
    const keys = Object.keys(tags);
    if (keys.length <= 0) {
        return undefined;
    }
    return tags;
};
const TagPills = ({ tags }) => {
    if (!tags) {
        return null;
    }
    const keys = Object.keys(tags);
    if (keys.length <= 0) {
        return null;
    }
    return (<pills_1.default>
      {keys.map((key, index) => (<pill_1.default key={index} name={key} value={String(tags[key]) || ''}/>))}
    </pills_1.default>);
};
const Tags = ({ baselineSpan, regressionSpan, }) => {
    const baselineTags = getTags(baselineSpan);
    const regressionTags = getTags(regressionSpan);
    if (!baselineTags && !regressionTags) {
        return null;
    }
    return (<RowSplitter>
      <RowContainer>
        <RowTitle>{(0, locale_1.t)('Tags')}</RowTitle>
        <div>
          <TagPills tags={baselineTags}/>
        </div>
      </RowContainer>
      <RowContainer>
        <RowTitle>{(0, locale_1.t)('Tags')}</RowTitle>
        <div>
          <TagPills tags={regressionTags}/>
        </div>
      </RowContainer>
    </RowSplitter>);
};
const DurationPill = (0, styled_1.default)('div') `
  position: absolute;
  top: 50%;
  display: flex;
  align-items: center;
  transform: translateY(-50%);
  white-space: nowrap;
  font-size: ${p => p.theme.fontSizeExtraSmall};
  color: ${p => p.fontColors.right};

  ${p => {
    switch (p.durationDisplay) {
        case 'right':
            return `left: calc(100% + ${(0, space_1.default)(0.75)});`;
        default:
            return `
          right: ${(0, space_1.default)(0.75)};
          color: ${p.fontColors.inset};
        `;
    }
}};

  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    font-size: 10px;
  }
`;
exports.default = SpanDetail;
//# sourceMappingURL=spanDetail.jsx.map