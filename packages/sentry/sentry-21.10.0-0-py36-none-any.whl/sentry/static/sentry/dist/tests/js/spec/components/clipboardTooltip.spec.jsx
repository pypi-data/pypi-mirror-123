Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const copy_text_to_clipboard_1 = (0, tslib_1.__importDefault)(require("copy-text-to-clipboard"));
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const clipboardTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/clipboardTooltip"));
jest.mock('copy-text-to-clipboard');
describe('ClipboardTooltip', function () {
    it('renders', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const title = 'tooltip content';
            const content = 'This text displays a tooltip when hovering';
            (0, reactTestingLibrary_1.mountWithTheme)(<clipboardTooltip_1.default title={title}>
        <span>{content}</span>
      </clipboardTooltip_1.default>);
            expect(reactTestingLibrary_1.screen.getByText(content)).toBeInTheDocument();
            reactTestingLibrary_1.fireEvent.mouseEnter(reactTestingLibrary_1.screen.getByText(content));
            yield reactTestingLibrary_1.screen.findByText(title);
            const clipboardContent = reactTestingLibrary_1.screen.getByLabelText('Copy to clipboard');
            expect(clipboardContent).toBeInTheDocument();
            reactTestingLibrary_1.fireEvent.click(clipboardContent);
            expect(copy_text_to_clipboard_1.default).toHaveBeenCalledWith(title);
        });
    });
});
//# sourceMappingURL=clipboardTooltip.spec.jsx.map