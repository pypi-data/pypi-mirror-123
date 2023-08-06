Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const is_prop_valid_1 = (0, tslib_1.__importDefault)(require("@emotion/is-prop-valid"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
class TagDistributionMeter extends React.Component {
    renderTitle() {
        const { segments, totalValues, title, isLoading, hasError, showReleasePackage } = this.props;
        if (!Array.isArray(segments) || segments.length <= 0) {
            return (<Title>
          <TitleType>{title}</TitleType>
        </Title>);
        }
        const largestSegment = segments[0];
        const pct = (0, utils_1.percent)(largestSegment.count, totalValues);
        const pctLabel = Math.floor(pct);
        const renderLabel = () => {
            switch (title) {
                case 'release':
                    return (<Label>
              <version_1.default version={largestSegment.name} anchor={false} tooltipRawVersion withPackage={showReleasePackage} truncate/>
            </Label>);
                default:
                    return <Label>{largestSegment.name || (0, locale_1.t)('n/a')}</Label>;
            }
        };
        return (<Title>
        <TitleType>{title}</TitleType>
        <TitleDescription>
          {renderLabel()}
          {isLoading || hasError ? null : <Percent>{pctLabel}%</Percent>}
        </TitleDescription>
      </Title>);
    }
    renderSegments() {
        const { segments, onTagClick, title, isLoading, hasError, totalValues, renderLoading, renderError, renderEmpty, showReleasePackage, } = this.props;
        if (isLoading) {
            return renderLoading();
        }
        if (hasError) {
            return <SegmentBar>{renderError()}</SegmentBar>;
        }
        if (totalValues === 0) {
            return <SegmentBar>{renderEmpty()}</SegmentBar>;
        }
        return (<SegmentBar>
        {segments.map((value, index) => {
                const pct = (0, utils_1.percent)(value.count, totalValues);
                const pctLabel = Math.floor(pct);
                const renderTooltipValue = () => {
                    switch (title) {
                        case 'release':
                            return (<version_1.default version={value.name} anchor={false} withPackage={showReleasePackage}/>);
                        default:
                            return value.name || (0, locale_1.t)('n/a');
                    }
                };
                const tooltipHtml = (<React.Fragment>
              <div className="truncate">{renderTooltipValue()}</div>
              {pctLabel}%
            </React.Fragment>);
                const segmentProps = {
                    index,
                    to: value.url,
                    onClick: () => {
                        if (onTagClick) {
                            onTagClick(title, value);
                        }
                    },
                };
                return (<div key={value.value} style={{ width: pct + '%' }}>
              <tooltip_1.default title={tooltipHtml} containerDisplayMode="block">
                {value.isOther ? <OtherSegment /> : <Segment {...segmentProps}/>}
              </tooltip_1.default>
            </div>);
            })}
      </SegmentBar>);
    }
    render() {
        const { segments, totalValues } = this.props;
        const totalVisible = segments.reduce((sum, value) => sum + value.count, 0);
        const hasOther = totalVisible < totalValues;
        if (hasOther) {
            segments.push({
                isOther: true,
                name: (0, locale_1.t)('Other'),
                value: 'other',
                count: totalValues - totalVisible,
                url: '',
            });
        }
        return (<TagSummary>
        {this.renderTitle()}
        {this.renderSegments()}
      </TagSummary>);
    }
}
exports.default = TagDistributionMeter;
TagDistributionMeter.defaultProps = {
    isLoading: false,
    hasError: false,
    renderLoading: () => null,
    renderEmpty: () => <p>{(0, locale_1.t)('No recent data.')}</p>,
    renderError: () => null,
    showReleasePackage: false,
};
const COLORS = [
    '#3A3387',
    '#5F40A3',
    '#8C4FBD',
    '#B961D3',
    '#DE76E4',
    '#EF91E8',
    '#F7B2EC',
    '#FCD8F4',
    '#FEEBF9',
];
const TagSummary = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(1)};
`;
const SegmentBar = (0, styled_1.default)('div') `
  display: flex;
  overflow: hidden;
  border-radius: 2px;
`;
const Title = (0, styled_1.default)('div') `
  display: flex;
  font-size: ${p => p.theme.fontSizeSmall};
  justify-content: space-between;
`;
const TitleType = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  font-weight: bold;
  ${overflowEllipsis_1.default};
`;
const TitleDescription = (0, styled_1.default)('div') `
  display: flex;
  color: ${p => p.theme.gray300};
  text-align: right;
`;
const Label = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default};
  max-width: 150px;
`;
const Percent = (0, styled_1.default)('div') `
  font-weight: bold;
  font-variant-numeric: tabular-nums;
  padding-left: ${(0, space_1.default)(0.5)};
  color: ${p => p.theme.textColor};
`;
const OtherSegment = (0, styled_1.default)('span') `
  display: block;
  width: 100%;
  height: 16px;
  color: inherit;
  outline: none;
  background-color: ${COLORS[COLORS.length - 1]};
`;
const Segment = (0, styled_1.default)(link_1.default, { shouldForwardProp: is_prop_valid_1.default }) `
  display: block;
  width: 100%;
  height: 16px;
  color: inherit;
  outline: none;
  background-color: ${p => COLORS[p.index]};
`;
//# sourceMappingURL=tagDistributionMeter.jsx.map