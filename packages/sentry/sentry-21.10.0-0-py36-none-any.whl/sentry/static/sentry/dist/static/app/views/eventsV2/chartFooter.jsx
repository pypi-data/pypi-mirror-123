Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const optionCheckboxSelector_1 = (0, tslib_1.__importDefault)(require("app/components/charts/optionCheckboxSelector"));
const optionSelector_1 = (0, tslib_1.__importDefault)(require("app/components/charts/optionSelector"));
const styles_1 = require("app/components/charts/styles");
const locale_1 = require("app/locale");
const types_1 = require("app/utils/discover/types");
function ChartFooter({ organization, total, yAxisValue, yAxisOptions, onAxisChange, displayMode, displayOptions, onDisplayChange, onTopEventsChange, topEvents, }) {
    const elements = [];
    elements.push(<styles_1.SectionHeading key="total-label">{(0, locale_1.t)('Total Events')}</styles_1.SectionHeading>);
    elements.push(total === null ? (<styles_1.SectionValue data-test-id="loading-placeholder" key="total-value">
        &mdash;
      </styles_1.SectionValue>) : (<styles_1.SectionValue key="total-value">{total.toLocaleString()}</styles_1.SectionValue>));
    const topEventOptions = [];
    for (let i = 1; i <= 10; i++) {
        topEventOptions.push({ value: i.toString(), label: i.toString() });
    }
    return (<styles_1.ChartControls>
      <styles_1.InlineContainer>{elements}</styles_1.InlineContainer>
      <styles_1.InlineContainer>
        <optionSelector_1.default title={(0, locale_1.t)('Display')} selected={displayMode} options={displayOptions} onChange={onDisplayChange} menuWidth="170px"/>
        <feature_1.default organization={organization} features={['discover-top-events']}>
          {({ hasFeature }) => {
            if (hasFeature && types_1.TOP_EVENT_MODES.includes(displayMode)) {
                return (<optionSelector_1.default title={(0, locale_1.t)('Limit')} selected={topEvents} options={topEventOptions} onChange={onTopEventsChange} menuWidth="60px" featureType="beta"/>);
            }
            else {
                return null;
            }
        }}
        </feature_1.default>
        <feature_1.default organization={organization} features={['connect-discover-and-dashboards']}>
          {({ hasFeature }) => {
            if (hasFeature) {
                return (<optionCheckboxSelector_1.default title={(0, locale_1.t)('Y-Axis')} selected={yAxisValue} options={yAxisOptions} onChange={onAxisChange}/>);
            }
            else {
                return (<optionSelector_1.default title={(0, locale_1.t)('Y-Axis')} selected={yAxisValue[0]} options={yAxisOptions} onChange={value => onAxisChange([value])}/>);
            }
        }}
        </feature_1.default>
      </styles_1.InlineContainer>
    </styles_1.ChartControls>);
}
exports.default = ChartFooter;
//# sourceMappingURL=chartFooter.jsx.map