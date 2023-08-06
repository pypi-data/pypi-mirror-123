Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
class AsyncView extends asyncComponent_1.default {
    getTitle() {
        return '';
    }
    render() {
        const title = this.getTitle();
        return (<react_document_title_1.default title={`${title ? `${title} - ` : ''}Sentry`}>
        {this.renderComponent()}
      </react_document_title_1.default>);
    }
}
exports.default = AsyncView;
//# sourceMappingURL=asyncView.jsx.map