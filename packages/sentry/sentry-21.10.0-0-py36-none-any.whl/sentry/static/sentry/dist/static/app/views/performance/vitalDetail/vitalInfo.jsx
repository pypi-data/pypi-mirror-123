Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const vitalsCardsDiscoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/vitals/vitalsCardsDiscoverQuery"));
const vitalsCards_1 = require("../landing/vitalsCards");
function vitalInfo(props) {
    const { vital, location, hideBar, hideStates, hideVitalPercentNames, hideDurationDetail, } = props;
    return (<vitalsCardsDiscoverQuery_1.default location={location} vitals={Array.isArray(vital) ? vital : [vital]}>
      {({ isLoading, vitalsData }) => (<vitalsCards_1.VitalBar isLoading={isLoading} data={vitalsData} vital={vital} showBar={!hideBar} showStates={!hideStates} showVitalPercentNames={!hideVitalPercentNames} showDurationDetail={!hideDurationDetail}/>)}
    </vitalsCardsDiscoverQuery_1.default>);
}
exports.default = vitalInfo;
//# sourceMappingURL=vitalInfo.jsx.map