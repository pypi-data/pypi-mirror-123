Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const locale_1 = require("app/locale");
const radioField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/radioField"));
const buildStep_1 = (0, tslib_1.__importDefault)(require("./buildStep"));
const utils_1 = require("./utils");
const dataSetChoices = [
    [utils_1.DataSet.EVENTS, (0, locale_1.t)('Events')],
    [utils_1.DataSet.METRICS, (0, locale_1.t)('Metrics')],
];
function ChooseDataSetStep({ value, onChange }) {
    return (<buildStep_1.default title={(0, locale_1.t)('Choose your data set')} description={(0, locale_1.t)('Monitor specific events such as errors and transactions or get metric readings on TBD.')}>
      <radioField_1.default name="dataSet" onChange={onChange} value={value} choices={dataSetChoices} inline={false} orientInline hideControlState stacked/>
    </buildStep_1.default>);
}
exports.default = ChooseDataSetStep;
//# sourceMappingURL=choseDataStep.jsx.map