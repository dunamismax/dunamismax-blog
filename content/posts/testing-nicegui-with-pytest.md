---
title: 'Bulletproof NiceGUI: Comprehensive Testing with Pytest'
date: 8/2/2025
time: 14:45
summary: Build reliable NiceGUI applications with comprehensive testing strategies covering unit tests, integration tests, and end-to-end UI validation using pytest and modern testing tools.
tags:
- nicegui
- pytest
- testing
- quality-assurance
- automation
- tdd
- python
---

# Bulletproof NiceGUI: Comprehensive Testing with Pytest

Building reliable web applications requires a robust testing strategy that catches bugs before they reach production. NiceGUI applications, with their unique blend of Python backend logic and reactive UI components, present interesting testing challenges that can be elegantly solved with pytest and modern testing practices.

This comprehensive guide explores proven testing strategies for NiceGUI applications, from unit testing business logic to end-to-end UI validation. We'll cover test organization, mock strategies, performance testing, and continuous integration patterns that ensure your applications remain reliable as they scale.

## **Why Testing Matters for NiceGUI Applications**

NiceGUI applications blur the traditional lines between frontend and backend testing. Your Python code directly manipulates UI elements, handles user interactions, and manages application state. This tight coupling creates opportunities for subtle bugs that only comprehensive testing can catch:

- **State Management Issues**: UI state that gets out of sync with business logic
- **Event Handler Failures**: Click handlers, form submissions, and async operations that fail silently
- **Route Registration Problems**: Pages that don't load or redirect incorrectly
- **Component Integration Bugs**: Custom components that don't interact properly
- **Performance Regressions**: Slow rendering or memory leaks in reactive components

A well-designed test suite catches these issues early and gives you confidence to refactor and extend your application.

## **Test Architecture and Organization**

### **Project Structure for Testing**

```bash
nicegui-project/
├── app/
│   ├── __init__.py
│   ├── main.py              # Main application
│   ├── components/          # Reusable UI components
│   ├── pages/              # Page modules
│   ├── services/           # Business logic
│   └── utils/              # Utility functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Pytest configuration
│   ├── unit/               # Unit tests
│   │   ├── test_services.py
│   │   ├── test_utils.py
│   │   └── test_components.py
│   ├── integration/        # Integration tests
│   │   ├── test_pages.py
│   │   └── test_workflows.py
│   ├── fixtures/           # Test data
│   │   ├── sample_posts.md
│   │   └── test_config.json
│   └── e2e/               # End-to-end tests
│       ├── test_user_flows.py
│       └── test_performance.py
├── pytest.ini             # Pytest configuration
└── requirements-test.txt   # Testing dependencies
```

### **Pytest Configuration**

```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --strict-config
    --verbose
    --cov=app
    --cov-report=html:htmlcov
    --cov-report=term-missing
    --cov-fail-under=85
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow tests that require special handling
    ui: Tests that involve UI components
    async: Async tests
```

## **Unit Testing Strategies**

### **Testing Business Logic**

```python
# tests/unit/test_content_service.py
import pytest
from datetime import datetime
from pathlib import Path
from app.services.content import ContentService, PostMetadata

class TestContentService:
    """Unit tests for content processing service."""
    
    @pytest.fixture
    def content_service(self):
        """Create a ContentService instance for testing."""
        return ContentService()
    
    @pytest.fixture
    def sample_markdown(self, tmp_path):
        """Create a temporary markdown file for testing."""
        content = """---
title: Test Post
date: 8/2/2025
time: 14:30
summary: A test post for unit testing
tags:
- test
- python
---

# Test Content

This is a test post with some **bold** text and a [link](https://example.com).

```python
def hello():
    return "world"
```

"""
        markdown_file = tmp_path / "test-post.md"
        markdown_file.write_text(content)
        return markdown_file

    def test_slug_generation(self, content_service):
        """Test URL slug generation from filenames."""
        test_cases = [
            ("my-awesome-post.md", "my-awesome-post"),
            ("Hello World Post.md", "hello-world-post"),
            ("Python_3.13_Tips.md", "python-313-tips"),
            ("Special!@#$%Characters.md", "specialcharacters"),
        ]
        
        for filename, expected_slug in test_cases:
            assert content_service.create_slug(filename) == expected_slug
    
    def test_slug_generation_edge_cases(self, content_service):
        """Test slug generation with edge cases."""
        with pytest.raises(ValueError, match="Filename must be a non-empty string"):
            content_service.create_slug("")
        
        with pytest.raises(ValueError, match="Filename must be a non-empty string"):
            content_service.create_slug(None)
    
    def test_markdown_processing(self, content_service, sample_markdown):
        """Test markdown to HTML conversion."""
        result = content_service.process_markdown_file(sample_markdown)
        
        # Check that HTML was generated
        assert result.html
        assert "<h1>Test Content</h1>" in result.html
        assert "<strong>bold</strong>" in result.html
        assert '<a href="https://example.com">link</a>' in result.html
        
        # Check code highlighting
        assert 'class="highlight"' in result.html
        
        # Check metadata extraction
        assert result.metadata['title'] == "Test Post"
        assert result.metadata['summary'] == "A test post for unit testing"
        assert 'test' in result.metadata['tags']
        assert 'python' in result.metadata['tags']
    
    def test_word_count_calculation(self, content_service, sample_markdown):
        """Test word count and reading time calculation."""
        result = content_service.process_markdown_file(sample_markdown)
        
        # Should count words in the content, excluding frontmatter
        assert result.word_count > 0
        assert result.read_time >= 1  # At least 1 minute reading time
        
        # Reading time should be based on ~200 words per minute
        expected_read_time = max(1, result.word_count // 200)
        assert result.read_time == expected_read_time
    
    def test_html_sanitization(self, content_service):
        """Test that dangerous HTML is sanitized."""
        dangerous_markdown = """

# Test Post

<script>alert('xss')</script>
<iframe src="javascript:alert('xss')"></iframe>

Normal content here.
"""
        result = content_service.process_markdown_content(dangerous_markdown)

        # Should remove dangerous tags
        assert "<script>" not in result.html
        assert "<iframe>" not in result.html
        assert "alert('xss')" not in result.html
        
        # Should preserve safe content
        assert "<h1>Test Post</h1>" in result.html
        assert "Normal content here" in result.html
    
    @pytest.mark.async
    async def test_async_content_loading(self, content_service, tmp_path):
        """Test async content loading with multiple files."""
        # Create multiple test files
        for i in range(5):
            content = f"""---

title: Post {i}
date: 8/2/2025
time: {14 + i}:00
---

# Post {i}

Content for post {i}
"""
            (tmp_path / f"post-{i}.md").write_text(content)

        # Load all posts asynchronously
        posts = await content_service.load_all_posts_async(tmp_path)
        
        assert len(posts) == 5
        
        # Should be sorted by date (newest first)
        for i, post in enumerate(posts):
            assert post.metadata['title'] == f'Post {4-i}'  # Reverse order

```

### **Testing Utility Functions**

```python
# tests/unit/test_utils.py
import pytest
from datetime import datetime
from app.utils.cache import TTLCacheManager
from app.utils.validators import validate_email, validate_url
from app.utils.formatters import format_date, truncate_text

class TestValidators:
    """Test input validation utilities."""
    
    @pytest.mark.parametrize("email,expected", [
        ("user@example.com", True),
        ("test.email+tag@domain.co.uk", True),
        ("invalid-email", False),
        ("@domain.com", False),
        ("user@", False),
        ("", False),
        (None, False),
    ])
    def test_email_validation(self, email, expected):
        """Test email validation with various inputs."""
        assert validate_email(email) == expected
    
    @pytest.mark.parametrize("url,expected", [
        ("https://example.com", True),
        ("http://localhost:8080", True),
        ("ftp://files.example.com", True),
        ("not-a-url", False),
        ("javascript:alert('xss')", False),
        ("", False),
        (None, False),
    ])
    def test_url_validation(self, url, expected):
        """Test URL validation with various inputs."""
        assert validate_url(url) == expected

class TestFormatters:
    """Test formatting utility functions."""
    
    def test_date_formatting(self):
        """Test date formatting utilities."""
        test_date = datetime(2025, 8, 2, 14, 30, 0)
        
        assert format_date(test_date, 'short') == "Aug 2, 2025"
        assert format_date(test_date, 'long') == "August 2, 2025"
        assert format_date(test_date, 'iso') == "2025-08-02"
    
    @pytest.mark.parametrize("text,length,expected", [
        ("Short text", 20, "Short text"),
        ("This is a longer text that should be truncated", 20, "This is a longer..."),
        ("", 10, ""),
        ("Exact", 5, "Exact"),
    ])
    def test_text_truncation(self, text, length, expected):
        """Test text truncation with various inputs."""
        assert truncate_text(text, length) == expected

class TestCacheManager:
    """Test caching utilities."""
    
    @pytest.fixture
    def cache_manager(self):
        """Create a cache manager for testing."""
        return TTLCacheManager(maxsize=10, ttl=1)
    
    def test_cache_basic_operations(self, cache_manager):
        """Test basic cache get/set operations."""
        # Test setting and getting values
        cache_manager.set('key1', 'value1')
        assert cache_manager.get('key1') == 'value1'
        
        # Test cache miss
        assert cache_manager.get('nonexistent') is None
        assert cache_manager.get('nonexistent', 'default') == 'default'
    
    @pytest.mark.async
    async def test_cache_ttl_expiration(self, cache_manager):
        """Test that cache entries expire after TTL."""
        import asyncio
        
        cache_manager.set('temp_key', 'temp_value')
        assert cache_manager.get('temp_key') == 'temp_value'
        
        # Wait for TTL to expire
        await asyncio.sleep(1.1)
        assert cache_manager.get('temp_key') is None
    
    def test_cache_size_limit(self, cache_manager):
        """Test that cache respects size limits."""
        # Fill cache to capacity
        for i in range(10):
            cache_manager.set(f'key{i}', f'value{i}')
        
        # Add one more item (should evict oldest)
        cache_manager.set('key10', 'value10')
        
        # First item should be evicted
        assert cache_manager.get('key0') is None
        assert cache_manager.get('key10') == 'value10'
```

## **Integration Testing**

### **Testing NiceGUI Components**

```python
# tests/integration/test_components.py
import pytest
from nicegui import ui, Client
from app.components.blog_card import BlogCard
from app.components.search_bar import SearchBar

class TestBlogCard:
    """Integration tests for BlogCard component."""
    
    @pytest.fixture
    def sample_post(self):
        """Sample post data for testing."""
        return {
            'title': 'Test Blog Post',
            'slug': 'test-blog-post',
            'summary': 'This is a test blog post summary',
            'date': '2025-08-02',
            'tags': ['test', 'python'],
            'read_time': 5,
            'word_count': 1000
        }
    
    def test_blog_card_rendering(self, sample_post):
        """Test that BlogCard renders correctly."""
        with Client() as client:
            card = BlogCard(sample_post)
            card.render()
            
            # Check that required elements are present
            # Note: In real tests, you might need to inspect the rendered HTML
            # or use NiceGUI's testing utilities
            assert card.post_data == sample_post
    
    def test_blog_card_click_navigation(self, sample_post):
        """Test that clicking the card navigates correctly."""
        with Client() as client:
            card = BlogCard(sample_post)
            card.render()
            
            # Simulate click and verify navigation
            # This would require NiceGUI's testing framework
            # or browser automation tools

class TestSearchBar:
    """Integration tests for SearchBar component."""
    
    def test_search_input_validation(self):
        """Test search input validation."""
        with Client() as client:
            search_bar = SearchBar()
            search_bar.render()
            
            # Test various search inputs
            test_queries = [
                ('python', True),
                ('a' * 100, False),  # Too long
                ('<script>', False),  # Contains HTML
                ('', True),  # Empty is valid
            ]
            
            for query, expected_valid in test_queries:
                result = search_bar.validate_query(query)
                assert result == expected_valid
    
    @pytest.mark.async
    async def test_search_debouncing(self):
        """Test that search requests are properly debounced."""
        import asyncio
        
        with Client() as client:
            search_bar = SearchBar(debounce_delay=0.1)
            search_bar.render()
            
            search_count = 0
            
            async def mock_search(query):
                nonlocal search_count
                search_count += 1
                return []
            
            search_bar.search_function = mock_search
            
            # Trigger multiple rapid searches
            await search_bar.on_input_change('p')
            await search_bar.on_input_change('py')
            await search_bar.on_input_change('pyt')
            await search_bar.on_input_change('pyth')
            await search_bar.on_input_change('pytho')
            await search_bar.on_input_change('python')
            
            # Wait for debounce period
            await asyncio.sleep(0.2)
            
            # Should only have triggered one search
            assert search_count == 1
```

### **Testing Page Routes and Navigation**

```python
# tests/integration/test_pages.py
import pytest
from nicegui import ui, Client
from app.main import create_app

class TestPageRoutes:
    """Test page route registration and basic functionality."""
    
    @pytest.fixture
    def app(self):
        """Create app instance for testing."""
        return create_app()
    
    def test_homepage_route(self, app):
        """Test that homepage route is registered."""
        routes = [route.path for route in app.routes]
        assert '/' in routes
    
    def test_blog_index_route(self, app):
        """Test that blog index route is registered."""
        routes = [route.path for route in app.routes]
        assert '/blog' in routes
    
    def test_blog_post_route(self, app):
        """Test that dynamic blog post route is registered."""
        routes = [route.path for route in app.routes]
        assert '/blog/{slug}' in routes
    
    @pytest.mark.async
    async def test_page_content_loading(self):
        """Test that pages load required content."""
        with Client() as client:
            # Test that blog index loads posts
            from app.pages.blog_index import load_blog_posts
            posts = await load_blog_posts()
            
            # Should return a list (even if empty)
            assert isinstance(posts, list)
    
    def test_404_error_handling(self, app):
        """Test that 404 errors are handled gracefully."""
        # This would require a test client that can make requests
        # and verify response codes
        pass

class TestPageComponents:
    """Test page-level component integration."""
    
    @pytest.mark.async
    async def test_blog_index_pagination(self):
        """Test blog index pagination functionality."""
        with Client() as client:
            from app.pages.blog_index import BlogIndexPage
            
            page = BlogIndexPage(posts_per_page=2)
            await page.load_posts()
            
            if len(page.all_posts) > 2:
                # Should have pagination controls
                assert page.has_pagination
                assert page.total_pages > 1
            else:
                # Should not have pagination
                assert not page.has_pagination
    
    @pytest.mark.async
    async def test_search_functionality(self):
        """Test search functionality across pages."""
        with Client() as client:
            from app.pages.blog_index import BlogIndexPage
            
            page = BlogIndexPage()
            await page.load_posts()
            
            # Test search with various queries
            if page.all_posts:
                # Search for existing content
                results = await page.search_posts('python')
                assert isinstance(results, list)
                
                # Search for non-existent content
                results = await page.search_posts('xyz123nonexistent')
                assert len(results) == 0
```

## **End-to-End Testing**

### **Browser-Based Testing with Playwright**

```python
# tests/e2e/test_user_flows.py
import pytest
from playwright.async_api import async_playwright, Page
import asyncio

@pytest.mark.e2e
class TestUserFlows:
    """End-to-end tests for complete user workflows."""
    
    @pytest.fixture
    async def browser_page(self):
        """Set up browser page for testing."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            yield page
            
            await context.close()
            await browser.close()
    
    @pytest.mark.async
    async def test_homepage_to_blog_navigation(self, browser_page: Page):
        """Test navigation from homepage to blog."""
        # Navigate to homepage
        await browser_page.goto('http://localhost:8080')
        
        # Should redirect to blog
        await browser_page.wait_for_url('**/blog')
        
        # Check that blog content is loaded
        await browser_page.wait_for_selector('.blog-post-card')
        
        # Verify page title
        title = await browser_page.title()
        assert 'Blog' in title
    
    @pytest.mark.async
    async def test_blog_post_reading_flow(self, browser_page: Page):
        """Test complete blog post reading flow."""
        # Go to blog index
        await browser_page.goto('http://localhost:8080/blog')
        
        # Wait for posts to load
        await browser_page.wait_for_selector('.blog-post-card')
        
        # Click on first blog post
        first_post_link = browser_page.locator('.blog-post-card a').first
        await first_post_link.click()
        
        # Should navigate to post detail page
        await browser_page.wait_for_url('**/blog/**')
        
        # Check that post content is loaded
        await browser_page.wait_for_selector('.blog-content')
        
        # Test scroll-to-top functionality
        await browser_page.evaluate('window.scrollTo(0, 1000)')
        scroll_button = browser_page.locator('.scroll-to-top')
        await scroll_button.wait_for(state='visible')
        await scroll_button.click()
        
        # Verify scroll position
        scroll_position = await browser_page.evaluate('window.pageYOffset')
        assert scroll_position == 0
    
    @pytest.mark.async
    async def test_search_functionality(self, browser_page: Page):
        """Test search functionality."""
        await browser_page.goto('http://localhost:8080/blog')
        
        # Wait for search input
        search_input = browser_page.locator('input[placeholder*="Search"]')
        await search_input.wait_for(state='visible')
        
        # Perform search
        await search_input.fill('python')
        await search_input.press('Enter')
        
        # Wait for results to update
        await asyncio.sleep(1)
        
        # Verify search results
        post_cards = browser_page.locator('.blog-post-card')
        count = await post_cards.count()
        
        # Should show relevant results (or handle no results gracefully)
        if count > 0:
            # Check that results contain search term
            first_card_text = await post_cards.first.text_content()
            assert 'python' in first_card_text.lower()
    
    @pytest.mark.async
    async def test_responsive_design(self, browser_page: Page):
        """Test responsive design on different screen sizes."""
        test_sizes = [
            (1920, 1080),  # Desktop
            (768, 1024),   # Tablet
            (375, 667),    # Mobile
        ]
        
        for width, height in test_sizes:
            await browser_page.set_viewport_size({'width': width, 'height': height})
            await browser_page.goto('http://localhost:8080/blog')
            
            # Check that navigation is accessible
            if width < 768:
                # Mobile: might have hamburger menu
                menu_button = browser_page.locator('[aria-label*="menu"]')
                if await menu_button.count() > 0:
                    await menu_button.click()
            
            # Verify content is visible and properly sized
            main_content = browser_page.locator('main')
            await main_content.wait_for(state='visible')
            
            # Check that text is readable (not too small)
            font_size = await browser_page.evaluate('''
                getComputedStyle(document.querySelector('main')).fontSize
            ''')
            
            font_size_px = int(font_size.replace('px', ''))
            assert font_size_px >= 14  # Minimum readable font size

@pytest.mark.e2e
class TestPerformance:
    """Performance testing for NiceGUI application."""
    
    @pytest.mark.async
    async def test_page_load_performance(self, browser_page: Page):
        """Test page load performance metrics."""
        # Start performance monitoring
        await browser_page.goto('http://localhost:8080/blog')
        
        # Measure page load timing
        timing = await browser_page.evaluate('''
            JSON.stringify(performance.timing)
        ''')
        
        import json
        timing_data = json.loads(timing)
        
        # Calculate metrics
        page_load_time = timing_data['loadEventEnd'] - timing_data['navigationStart']
        dom_ready_time = timing_data['domContentLoadedEventEnd'] - timing_data['navigationStart']
        
        # Assert performance thresholds
        assert page_load_time < 3000  # Page should load within 3 seconds
        assert dom_ready_time < 2000  # DOM should be ready within 2 seconds
    
    @pytest.mark.async
    async def test_memory_usage(self, browser_page: Page):
        """Test memory usage patterns."""
        # Navigate to pages and monitor memory
        pages_to_test = [
            'http://localhost:8080/blog',
            'http://localhost:8080/blog/welcome-to-my-blog',
            'http://localhost:8080/blog/python-tips-and-tricks',
        ]
        
        for url in pages_to_test:
            await browser_page.goto(url)
            await browser_page.wait_for_load_state('networkidle')
            
            # Get memory usage
            memory_info = await browser_page.evaluate('''
                new Promise(resolve => {
                    if (performance.memory) {
                        resolve({
                            usedJSHeapSize: performance.memory.usedJSHeapSize,
                            totalJSHeapSize: performance.memory.totalJSHeapSize
                        });
                    } else {
                        resolve(null);
                    }
                })
            ''')
            
            if memory_info:
                # Memory usage should be reasonable (less than 50MB)
                memory_mb = memory_info['usedJSHeapSize'] / (1024 * 1024)
                assert memory_mb < 50, f"Memory usage too high: {memory_mb:.2f}MB"
```

## **Testing Async Operations**

```python
# tests/integration/test_async_operations.py
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from app.services.api_client import APIClient
from app.services.background_tasks import BackgroundTaskManager

class TestAsyncOperations:
    """Test async operations and background tasks."""
    
    @pytest.mark.async
    async def test_api_client_retry_logic(self):
        """Test API client retry logic with failures."""
        api_client = APIClient()
        
        # Mock that fails twice then succeeds
        call_count = 0
        async def mock_request(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Network error")
            return {"status": "success"}
        
        with patch.object(api_client, '_make_request', side_effect=mock_request):
            result = await api_client.get_data('/api/posts')
            
            assert result["status"] == "success"
            assert call_count == 3  # Should have retried twice
    
    @pytest.mark.async
    async def test_background_task_execution(self):
        """Test background task execution and error handling."""
        task_manager = BackgroundTaskManager()
        
        results = []
        errors = []
        
        async def success_task():
            await asyncio.sleep(0.1)
            results.append("success")
        
        async def failing_task():
            await asyncio.sleep(0.1)
            raise ValueError("Task failed")
        
        # Schedule tasks
        task_manager.schedule(success_task())
        task_manager.schedule(failing_task())
        
        # Set up error handler
        task_manager.on_error = lambda error: errors.append(str(error))
        
        # Wait for tasks to complete
        await task_manager.wait_for_completion()
        
        assert len(results) == 1
        assert len(errors) == 1
        assert "Task failed" in errors[0]
    
    @pytest.mark.async
    async def test_concurrent_cache_operations(self):
        """Test cache behavior under concurrent access."""
        from app.utils.cache import TTLCacheManager
        
        cache = TTLCacheManager(maxsize=100, ttl=1)
        
        async def write_operation(key, value):
            cache.set(key, value)
            await asyncio.sleep(0.01)  # Simulate work
            return cache.get(key)
        
        async def read_operation(key):
            await asyncio.sleep(0.01)  # Simulate work
            return cache.get(key)
        
        # Run concurrent operations
        tasks = []
        for i in range(10):
            tasks.append(write_operation(f'key{i}', f'value{i}'))
            tasks.append(read_operation(f'key{i}'))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Should not have any exceptions
        exceptions = [r for r in results if isinstance(r, Exception)]
        assert len(exceptions) == 0
```

## **Mock Strategies and Test Doubles**

```python
# tests/conftest.py
import pytest
from unittest.mock import Mock, AsyncMock, patch
import tempfile
from pathlib import Path

@pytest.fixture
def mock_file_system(tmp_path):
    """Create a mock file system for testing."""
    # Create sample blog posts
    posts_dir = tmp_path / "posts"
    posts_dir.mkdir()
    
    sample_posts = [
        {
            "filename": "welcome-post.md",
            "content": """---
title: Welcome Post
date: 8/2/2025
time: 14:00
summary: Welcome to the blog
tags: [welcome, test]
---

# Welcome
This is the welcome post content.
"""
        },
        {
            "filename": "python-tips.md",
            "content": """---
title: Python Tips
date: 8/1/2025
time: 10:00
summary: Useful Python tips
tags: [python, tips]
---

# Python Tips
Here are some useful Python tips.
"""
        }
    ]
    
    for post in sample_posts:
        (posts_dir / post["filename"]).write_text(post["content"])
    
    return posts_dir

@pytest.fixture
def mock_api_responses():
    """Mock external API responses."""
    responses = {
        '/api/posts': [
            {'id': 1, 'title': 'Post 1', 'content': 'Content 1'},
            {'id': 2, 'title': 'Post 2', 'content': 'Content 2'},
        ],
        '/api/users/123': {'id': 123, 'name': 'Test User', 'email': 'test@example.com'},
    }
    
    async def mock_get(url):
        return responses.get(url, {})
    
    with patch('httpx.AsyncClient.get', side_effect=mock_get):
        yield responses

@pytest.fixture
def mock_cache():
    """Mock cache for testing without Redis dependency."""
    cache_data = {}
    
    class MockCache:
        def get(self, key, default=None):
            return cache_data.get(key, default)
        
        def set(self, key, value, ttl=None):
            cache_data[key] = value
        
        def delete(self, key):
            cache_data.pop(key, None)
        
        def clear(self):
            cache_data.clear()
        
        def exists(self, key):
            return key in cache_data
    
    return MockCache()

@pytest.fixture
def mock_database():
    """Mock database for testing without actual DB connection."""
    db_data = {
        'posts': [],
        'users': [],
        'comments': []
    }
    
    class MockDB:
        async def execute(self, query, *args):
            # Simple mock that returns success
            return {'affected_rows': 1}
        
        async def fetch_all(self, query, *args):
            # Return relevant mock data based on query
            if 'posts' in query.lower():
                return db_data['posts']
            elif 'users' in query.lower():
                return db_data['users']
            return []
        
        async def fetch_one(self, query, *args):
            results = await self.fetch_all(query, *args)
            return results[0] if results else None
    
    return MockDB()
```

## **Continuous Integration and Testing Automation**

### **GitHub Actions Workflow**

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11, 3.12, 3.13]
    
    services:
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install UV
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        echo "$HOME/.cargo/bin" >> $GITHUB_PATH
    
    - name: Install dependencies
      run: |
        uv sync --dev
    
    - name: Run linting
      run: |
        uv run ruff check .
        uv run ruff format --check .
    
    - name: Run type checking
      run: |
        uv run mypy .
    
    - name: Run unit tests
      run: |
        uv run pytest tests/unit/ -v --cov=app --cov-report=xml
    
    - name: Run integration tests
      run: |
        uv run pytest tests/integration/ -v
    
    - name: Install Playwright
      run: |
        uv run playwright install --with-deps chromium
    
    - name: Start application
      run: |
        uv run python app/main.py &
        sleep 10  # Wait for app to start
      env:
        ENVIRONMENT: test
        REDIS_URL: redis://localhost:6379
    
    - name: Run E2E tests
      run: |
        uv run pytest tests/e2e/ -v --maxfail=3
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: true

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run security scan
      run: |
        pip install bandit safety
        bandit -r app/
        safety check
```

## **Performance and Load Testing**

```python
# tests/performance/test_load.py
import pytest
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
import httpx

@pytest.mark.slow
class TestLoadPerformance:
    """Load testing for NiceGUI application."""
    
    @pytest.mark.async
    async def test_concurrent_page_loads(self):
        """Test application under concurrent load."""
        base_url = "http://localhost:8080"
        endpoints = [
            "/blog",
            "/blog/welcome-to-my-blog",
            "/blog/python-tips-and-tricks",
        ]
        
        async def load_endpoint(client, endpoint):
            start_time = time.time()
            response = await client.get(f"{base_url}{endpoint}")
            end_time = time.time()
            
            return {
                'endpoint': endpoint,
                'status_code': response.status_code,
                'response_time': end_time - start_time,
                'content_length': len(response.content)
            }
        
        # Simulate 50 concurrent users
        concurrent_requests = 50
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            tasks = []
            for _ in range(concurrent_requests):
                for endpoint in endpoints:
                    tasks.append(load_endpoint(client, endpoint))
            
            start_time = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            total_time = time.time() - start_time
        
        # Analyze results
        successful_requests = [r for r in results if not isinstance(r, Exception)]
        failed_requests = [r for r in results if isinstance(r, Exception)]
        
        success_rate = len(successful_requests) / len(results)
        avg_response_time = sum(r['response_time'] for r in successful_requests) / len(successful_requests)
        
        # Performance assertions
        assert success_rate >= 0.95, f"Success rate too low: {success_rate:.2%}"
        assert avg_response_time < 2.0, f"Average response time too high: {avg_response_time:.2f}s"
        assert len(failed_requests) == 0, f"Failed requests: {failed_requests}"
        
        print(f"Load test completed:")
        print(f"  Total requests: {len(results)}")
        print(f"  Success rate: {success_rate:.2%}")
        print(f"  Average response time: {avg_response_time:.2f}s")
        print(f"  Total test time: {total_time:.2f}s")
    
    @pytest.mark.async
    async def test_memory_usage_under_load(self):
        """Test memory usage during sustained load."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Simulate sustained load
        base_url = "http://localhost:8080"
        
        async with httpx.AsyncClient() as client:
            for i in range(100):
                await client.get(f"{base_url}/blog")
                
                if i % 25 == 0:
                    current_memory = process.memory_info().rss / 1024 / 1024
                    memory_increase = current_memory - initial_memory
                    
                    # Memory shouldn't grow too much
                    assert memory_increase < 100, f"Memory leak detected: {memory_increase:.2f}MB increase"
        
        final_memory = process.memory_info().rss / 1024 / 1024
        total_increase = final_memory - initial_memory
        
        print(f"Memory usage:")
        print(f"  Initial: {initial_memory:.2f}MB")
        print(f"  Final: {final_memory:.2f}MB")
        print(f"  Increase: {total_increase:.2f}MB")
```

## **Testing Best Practices**

### **Test Organization and Naming**

```python
# Good test naming examples
def test_slug_generation_with_special_characters():
    """Test that special characters are properly handled in slug generation."""
    pass

def test_cache_expires_after_ttl_timeout():
    """Test that cache entries are automatically removed after TTL expires."""
    pass

def test_search_returns_relevant_results_for_python_query():
    """Test that searching for 'python' returns posts containing python content."""
    pass

# Test data builders
class PostBuilder:
    """Builder pattern for creating test post data."""
    
    def __init__(self):
        self.data = {
            'title': 'Test Post',
            'slug': 'test-post',
            'content': 'Test content',
            'tags': [],
            'date': '2025-08-02',
            'time': '14:00'
        }
    
    def with_title(self, title: str):
        self.data['title'] = title
        return self
    
    def with_tags(self, tags: list[str]):
        self.data['tags'] = tags
        return self
    
    def with_content(self, content: str):
        self.data['content'] = content
        return self
    
    def build(self):
        return self.data.copy()

# Usage in tests
def test_post_with_multiple_tags():
    post = PostBuilder().with_title("Python Tips").with_tags(["python", "tips", "coding"]).build()
    assert len(post['tags']) == 3
```

### **Assertion Strategies**

```python
# Good assertion examples
def test_blog_post_content_processing():
    """Test comprehensive post processing."""
    result = process_blog_post(sample_markdown)
    
    # Multiple specific assertions instead of one large one
    assert result.title == "Expected Title"
    assert result.word_count > 0
    assert result.read_time >= 1
    assert "python" in result.tags
    assert "<script>" not in result.html  # Security check
    assert result.summary is not None

# Custom assertion helpers
def assert_valid_html(html_content: str):
    """Assert that HTML content is valid and safe."""
    from bs4 import BeautifulSoup
    
    # Should parse without errors
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Should not contain dangerous elements
    dangerous_tags = soup.find_all(['script', 'iframe', 'object', 'embed'])
    assert len(dangerous_tags) == 0, f"Dangerous HTML tags found: {dangerous_tags}"
    
    return soup

def assert_performance_within_threshold(operation_time: float, threshold: float):
    """Assert that operation completed within performance threshold."""
    assert operation_time <= threshold, f"Operation took {operation_time:.2f}s, expected <= {threshold}s"
```

## **Running Tests Efficiently**

### **Test Selection and Filtering**

```bash
# Run specific test categories
uv run pytest tests/unit/                    # Unit tests only
uv run pytest tests/integration/             # Integration tests only
uv run pytest -m "not slow"                 # Skip slow tests
uv run pytest -m "ui and not e2e"          # UI tests but not E2E

# Run tests with specific patterns
uv run pytest -k "test_cache"              # Run cache-related tests
uv run pytest tests/ -k "not performance"  # Skip performance tests

# Parallel test execution
uv run pytest -n auto                      # Auto-detect CPU cores
uv run pytest -n 4                         # Use 4 processes

# Debugging options
uv run pytest -vvv --tb=long              # Verbose output with full tracebacks
uv run pytest --pdb                       # Drop into debugger on failure
uv run pytest -x                          # Stop on first failure
```

### **Test Coverage and Reporting**

```bash
# Generate coverage reports
uv run pytest --cov=app --cov-report=html
uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=85

# Generate test report with timing
uv run pytest --durations=10              # Show 10 slowest tests
```

## **Conclusion**

Comprehensive testing is essential for building reliable NiceGUI applications. A well-designed test suite provides confidence to refactor, prevents regressions, and serves as living documentation of your application's behavior.

Key principles for effective NiceGUI testing:

1. **Test Pyramid**: More unit tests, fewer integration tests, minimal E2E tests
2. **Fast Feedback**: Unit tests should run in milliseconds, full suite under 2 minutes
3. **Realistic Mocking**: Mock external dependencies but preserve business logic behavior
4. **Clear Assertions**: Each test should verify one specific behavior
5. **Maintainable Tests**: Tests should be as clean and well-structured as production code

Start with unit tests for your business logic, add integration tests for component interactions, and use E2E tests sparingly for critical user workflows. With proper testing in place, you can deploy NiceGUI applications with confidence, knowing that your users will have a reliable, bug-free experience.
