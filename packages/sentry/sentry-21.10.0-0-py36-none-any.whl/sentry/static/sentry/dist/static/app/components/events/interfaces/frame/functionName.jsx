Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const locale_1 = require("app/locale");
const FunctionName = (_a) => {
    var { frame, showCompleteFunctionName, hasHiddenDetails, className } = _a, props = (0, tslib_1.__rest)(_a, ["frame", "showCompleteFunctionName", "hasHiddenDetails", "className"]);
    const getValueOutput = () => {
        if (hasHiddenDetails && showCompleteFunctionName && frame.rawFunction) {
            return {
                value: frame.rawFunction,
                meta: (0, metaProxy_1.getMeta)(frame, 'rawFunction'),
            };
        }
        if (frame.function) {
            return {
                value: frame.function,
                meta: (0, metaProxy_1.getMeta)(frame, 'function'),
            };
        }
        if (frame.rawFunction) {
            return {
                value: frame.rawFunction,
                meta: (0, metaProxy_1.getMeta)(frame, 'rawFunction'),
            };
        }
        return undefined;
    };
    const valueOutput = getValueOutput();
    return (<code className={className} {...props}>
      {!valueOutput ? ((0, locale_1.t)('<unknown>')) : (<annotatedText_1.default value={valueOutput.value} meta={valueOutput.meta}/>)}
    </code>);
};
exports.default = FunctionName;
//# sourceMappingURL=functionName.jsx.map