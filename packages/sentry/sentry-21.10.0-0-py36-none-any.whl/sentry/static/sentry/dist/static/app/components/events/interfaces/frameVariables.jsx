Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const keyValueList_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/keyValueList"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const FrameVariables = ({ data }) => {
    // make sure that clicking on the variables does not actually do
    // anything on the containing element.
    const handlePreventToggling = () => (event) => {
        event.stopPropagation();
    };
    const getTransformedData = () => {
        const transformedData = [];
        const dataKeys = Object.keys(data).reverse();
        for (const key of dataKeys) {
            transformedData.push({
                key,
                subject: key,
                value: data[key],
                meta: (0, metaProxy_1.getMeta)(data, key),
            });
        }
        return transformedData;
    };
    const transformedData = getTransformedData();
    return (<keyValueList_1.default data={transformedData} onClick={handlePreventToggling} isContextData/>);
};
exports.default = FrameVariables;
//# sourceMappingURL=frameVariables.jsx.map