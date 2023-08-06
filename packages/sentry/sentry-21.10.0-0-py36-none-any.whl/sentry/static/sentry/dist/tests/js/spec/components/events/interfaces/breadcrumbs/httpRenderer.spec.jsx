Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const http_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/breadcrumbs/breadcrumb/data/http"));
const breadcrumbs_1 = require("app/types/breadcrumbs");
describe('HttpRenderer', () => {
    describe('render', () => {
        it('should work', () => {
            const httpRendererWrapper = (0, enzyme_1.mountWithTheme)(<http_1.default searchTerm="" breadcrumb={{
                    type: breadcrumbs_1.BreadcrumbType.HTTP,
                    level: breadcrumbs_1.BreadcrumbLevelType.INFO,
                    data: {
                        method: 'POST',
                        url: 'http://example.com/foo',
                        // status_code 0 is possible via broken client-side XHR; should still render as '[0]'
                        status_code: 0,
                    },
                }}/>);
            const annotatedTexts = httpRendererWrapper.find('AnnotatedText');
            expect(annotatedTexts.length).toEqual(3);
            expect(annotatedTexts.at(0).find('strong').text()).toEqual('POST ');
            expect(annotatedTexts.at(1).find('a[data-test-id="http-renderer-external-link"]').text()).toEqual('http://example.com/foo');
            expect(annotatedTexts
                .at(2)
                .find('Highlight[data-test-id="http-renderer-status-code"]')
                .text()).toEqual(' [0]');
        });
        it("shouldn't blow up if crumb.data is missing", () => {
            const httpRendererWrapper = (0, enzyme_1.mountWithTheme)(<http_1.default searchTerm="" breadcrumb={{
                    category: 'xhr',
                    type: breadcrumbs_1.BreadcrumbType.HTTP,
                    level: breadcrumbs_1.BreadcrumbLevelType.INFO,
                }}/>);
            const annotatedTexts = httpRendererWrapper.find('AnnotatedText');
            expect(annotatedTexts.length).toEqual(0);
        });
        it("shouldn't blow up if url is not a string", () => {
            const httpRendererWrapper = (0, enzyme_1.mountWithTheme)(<http_1.default searchTerm="" breadcrumb={{
                    category: 'xhr',
                    type: breadcrumbs_1.BreadcrumbType.HTTP,
                    level: breadcrumbs_1.BreadcrumbLevelType.INFO,
                    data: {
                        method: 'GET',
                    },
                }}/>);
            const annotatedTexts = httpRendererWrapper.find('AnnotatedText');
            expect(annotatedTexts.length).toEqual(1);
        });
    });
});
//# sourceMappingURL=httpRenderer.spec.jsx.map