Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const indicators_1 = (0, tslib_1.__importDefault)(require("app/components/indicators"));
const themeAndStyleProvider_1 = (0, tslib_1.__importDefault)(require("app/components/themeAndStyleProvider"));
const awsLambdaCloudformation_1 = (0, tslib_1.__importDefault)(require("./awsLambdaCloudformation"));
const awsLambdaFailureDetails_1 = (0, tslib_1.__importDefault)(require("./awsLambdaFailureDetails"));
const awsLambdaFunctionSelect_1 = (0, tslib_1.__importDefault)(require("./awsLambdaFunctionSelect"));
const awsLambdaProjectSelect_1 = (0, tslib_1.__importDefault)(require("./awsLambdaProjectSelect"));
const pipelineMapper = {
    awsLambdaProjectSelect: [awsLambdaProjectSelect_1.default, 'AWS Lambda Select Project'],
    awsLambdaFunctionSelect: [awsLambdaFunctionSelect_1.default, 'AWS Lambda Select Lambdas'],
    awsLambdaCloudformation: [awsLambdaCloudformation_1.default, 'AWS Lambda Create Cloudformation'],
    awsLambdaFailureDetails: [awsLambdaFailureDetails_1.default, 'AWS Lambda View Failures'],
};
/**
 * This component is a wrapper for specific pipeline views for integrations
 */
function PipelineView(_a) {
    var { pipelineName } = _a, props = (0, tslib_1.__rest)(_a, ["pipelineName"]);
    const mapping = pipelineMapper[pipelineName];
    if (!mapping) {
        throw new Error(`Invalid pipeline name ${pipelineName}`);
    }
    const [Component, title] = mapping;
    // Set the page title
    (0, react_1.useEffect)(() => void (document.title = title), [title]);
    return (<themeAndStyleProvider_1.default>
      <indicators_1.default className="indicators-container"/>
      <Component {...props}/>
    </themeAndStyleProvider_1.default>);
}
exports.default = PipelineView;
//# sourceMappingURL=pipelineView.jsx.map