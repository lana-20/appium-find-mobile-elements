# Finding Mobile Elements with Appium

*Finding UI elements with Appium is more or less the same as finding them with Selenium, but we have access to a different set of locator strategies, which means different selectors to think about, too.*

Now we come to finding mobile UI elements using Appium. In general, finding elements works the same way on mobile as on browsers, but there are some important differences.

Just like with web elements, finding mobile elements is a combination of locator strategies and selectors. Let's take a look at the locator strategies available with Appium for iOS and Android.

First, let's talk about the one strategy which is in common between Selenium and Appium, namely the XPath locator strategy. XPath works the same way on mobile, but the XML documents which act as the basis for the queries are very different. In fact, they are not only different from HTML, they are different from one another. That is to say, if you get the page source of an iOS app and the page source of an Android app, they don't use any of the same XML tags. Why are things this way? Well, neither iOS nor Android really have a page source to begin with. Appium just generates one for us so that we can look at it, and so that we can use XPath queries. For this reason, XPath is not a cross-platform locator strategy. If you write an XPath query for iOS, it will probably not work with Android without modification. There are lots of reasons not to use XPath with Appium if you can help it, but we'll talk about that in a bit.

Next, let's move on to the Accessibility ID locator strategy. This is my preferred locator strategy. What does "Accessibility ID" mean? Well, both iOS and Android have the concept of an Accessibility system, which modifies the way the device works to assist users who might find it difficult to use the device in its default mode. People who have trouble seeing or reading small text, for example, can turn on a device mode where they can navigate views purely by moving their fingers around and having element labels read out to them. Developers can attach these labels to elements when they design apps, to make their apps more accessible. On iOS these labels are called Accessibility Labels, and on Android they're called Content Descriptions.

Eventually Apple realized that people like to do UI tests of applications, and were using Accessibility Label data to assist in their testing. But this is not what Accessibility Labels were designed for. To complicate things, Accessibility Labels are often localized, in other words, they are designed to show up in the language of the user, which is an unnecessary complication for running UI tests unless you're testing localization specifically. So Apple created the concept of an Accessibility ID, which is another string that developers can add, which are not visible to users but only to UI automation processes, like Appium. All this to say, Accessibility IDs are little strings that app developers can assign to elements, and that you can use to find elements with in Appium on iOS.

On Android, there's not this distinction between external and internal accessibility strings. Instead, there's the single concept of Content Description, which is definitely an outward-facing accessibility label. Appium can still find elements by these labels, however. So if you use the Accessibility ID locator strategy, you are finding elements by Accessibility ID on iOS and Content Description on Android.

The great thing about this locator strategy is that it has the potential to be totally cross-platform! If you have an iOS and an Android version of your app, you can develop them in such a way that the equivalent elements for each app have the same Accessibility ID and Content Description. Then you can use the same find element commands regardless of which app you're automating.

The third basic locator strategy is the 'class name' strategy. It basically allows you to do the equivalent of what the 'tag name' strategy allows you to do in Selenium, namely finding elements by their type. There are no such things as tags in mobile apps, since the UI elements are not HTML elements. But the UI elements do belong to certain UI element classes as defined in the iOS or Android SDKs. For example, an Android button has the class name <code>android.widget.Button</code>. When you retrieve the page source for a mobile app, the XML nodes are populated using the UI element class names, so that's a good way to explore the various classes.

The last basic strategy is the 'id' strategy. This one is a bit tricky. It exists primarily for use on the Android platform, because Android elements can be associated with something called an Android ID. This is an internal-only identifier used to refer to elements, though there is no requirement that the ID be unique. Still, Android IDs are a common way for Android developers to refer internally to elements, and Appium allows you to find them using this strategy. But what if you use this strategy on iOS? Well, on iOS this strategy will just do the same thing that the Accessibility ID strategy does--it will look for elements by their accessibility ID. For this reason, to make it clear exactly what your test code is doing, I recommend only using the 'id' strategy for Android.

In the last slide, you may have noticed that all the locator strategies started with the word MobileBy. This is the Appium equivalent of Selenium's By class. We use it just the same way as we do the By class, in order to find the locator strategies that Appium supports. You can see on this slide how we import it, from the package appium.webdriver.common.mobileby. Appium keeps all the original Selenium strategies on the MobileBy class as well so you can safely import it alone even if you're writing web tests too.

OK, now let's pause for a moment to consider XPath, and why we might want to avoid using it, or at least, use it wisely.

We already mentioned in connection with finding elements for web that using XPath could encourage the use of unstable selectors. That also applies to Appium. Using path-based selectors can lead to brittle test code, which breaks unexpectedly just because random little things changed in the UI structure.

For Appium, there's another set of reasons not to use XPath. The first is that XPath selectors are not cross-platform, usually. It is difficult to write a single XPath query that will work on both iOS and Android, since the element class names and attributes differ so greatly.

Furthermore, XPath in Appium can be quite costly in terms of test performance. This is because there is no native XML or XPath search functionality for iOS or Android. To support XPath, Appium has to first serialize an XML document from the set of available elements, which means recursively finding and looking at every element on screen. Then, it has to perform the XPath query itself (which is pretty fast). Then, it has to take any matching nodes and connect them back up with actual UI elements, which were never part of the XML document. In other words, Appium has to do a lot of extra work to make your XPath query match mobile elements, and in some cases, especially depending on how many elements are on screen, this can take a very long time.

All that being said, there are some cases where it's OK to use XPath, as long as we do it wisely. What does it look like to use XPath wisely?

First, it looks like using it as a last resort. It's definitely better to use one of the ID strategies if possible, since those will be much faster and easier to maintain.

Second, it looks like making sure your selectors aren't brittle by ensuring they are keyed to unique element properties. So something like //element[@prop='unique_value'] instead of //element/element/element. This is where a deep knowledge of XPath helps, because there is often a way to intelligently refer to an element using unique information about it, or its parents, children, or siblings.

Third, it looks like doing extensive performance testing of your query to make sure it's not slowing down your test too much. If you have a "normal" app without too many elements on screen, XPath is going to be fine. But it's always important to test this before you add a bunch of queries to your testsuite. You might even find that as your app grows and elements are added, existing queries might slow down.

Alright, let's look at a quick set of examples. It's basically exactly the same as for Selenium, just that we are using mobile locator strategies. For the find_element call we are using MobileBy.ACCESSIBILITY_ID, and for the find_elements call we are using MobileBy.ID.

Now seems like a good time to put this into practice! So let's head on over to our editor. Alright. Let's work up an example of finding elements on iOS. I'm going to create a new file called [<code>find_ios.py</code>](https://github.com/lana-20/appium-find-mobile-elements/blob/main/find_ios.py):

    from os import path
    from appium import webdriver
    from appium.webdriver.common.mobileby import MobileBy
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    CUR_DIR = path.dirname(path.abspath(__file__))
    APP = path.join(CUR_DIR, 'TheApp.app.zip')
    APPIUM = 'http://localhost:4723'
    CAPS = {
        'platformName': 'iOS',
        'platformVersion': '16.2',
        'deviceName': 'iPhone 14 Pro',
        'automationName': 'XCUITest',
        'app': APP,
    }

    driver = webdriver.Remote(APPIUM, CAPS)
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(
            (MobileBy.ACCESSIBILITY_ID, 'Login Screen')))
        driver.find_element(MobileBy.CLASS_NAME, 'XCUIElementTypeStaticText')
        driver.find_element(MobileBy.XPATH, '//XCUIElementTypeOther[@label="Webview Demo"]')
    finally:
        driver.quit()

The first thing we do in this script is import our wait and expected conditions modules, since we're going to use them with Appium just like we did with Selenium. We'll also want our <code>MobileBy</code> class so we can use it to get the locator strategies we'll use.

    from appium.webdriver.common.mobileby import MobileBy
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

I put the <code>driver.quit</code> line into a <code>finally</code> block to recognize that all our actual driver usage is going to go inside some exception handling:

    driver = webdriver.Remote(APPIUM, CAPS)
    try:
    finally:
        driver.quit()

Now it's time to find an element. But as we know, it's a good practice not to just find an element right off the bat, because we know that an app could take some time to load its elements. Thus we want to use a WebDriverWait! All of this will go inside the <code>try</code> block:

    wait = WebDriverWait(driver, 10)

Now that we have a wait, we can use it to wait for an element. I'm going to try to find an element by Accessibility ID. In this case I'm going to try to find the 'Login Screen' element, which is basically a list item that when tapped will take us to the Login Screen. So I will use <code>MobileBy.ACCESSIBILITY_ID</code>:

    wait.until(EC.presence_of_element_located(
            (MobileBy.ACCESSIBILITY_ID, 'Login Screen')))

I'm not actually doing anything with the element in this script, which is why I'm not assigning anything with the return value of <code>wait.until</code>. At this point in the script, if this line doesn't raise an exception, we will know that we've found this Login Screen element.

Let's not stop here! Let's try to find a few more elements as well. Now that I'm on the screen, I don't need to wait anymore because I know that if we've found the Login Screen element, all the others on this screen will be loaded as well. So let's try and find an element by its type, in other words, by its class name.

    driver.find_element(MobileBy.CLASS_NAME, 'XCUIElementTypeStaticText')

Here I'm just using <code>find_element</code>, and the type of element I'm finding is an <code>XCUIElementTypeStaticText</code>. This is iOS's verbose way of denoting the class name of a static text field, i.e., a simple text label. Let's do one more too.

    driver.find_element(MobileBy.XPATH, '//XCUIElementTypeOther[@label="Webview Demo"]')

This time I'm using XPath, to try and find an element which has the label of "Webview Demo". I'll save this file, then head over to my terminal to execute it with the <code>python</code> or <code>python**3**</code> command. As always, I need to ensure that I have an Appium server running, and it helps also to make sure I have the appropriate simulator already launched, though it's not necessary. 

All we see as this executes is that the app pops open and then almost immediately closes again. As long as there was nothing printed out to my terminal, that's great. That's what we want. It means all the elements were found correctly.

Let's head back to the editor and do the same thing for Android in the [<code>find_android.py</code>](https://github.com/lana-20/appium-find-mobile-elements/blob/main/find_android.py) file:

    from os import path
    from appium import webdriver
    from appium.webdriver.common.mobileby import MobileBy
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    CUR_DIR = path.dirname(path.abspath(__file__))
    APP = path.join(CUR_DIR, 'TheApp-v1.10.0.apk')
    APPIUM = 'http://localhost:4723'
    CAPS = {
        'platformName': 'Android',
        'platformVersion': '13.2',
        'deviceName': 'Android Emulator',
        'automationName': 'UiAutomator2',
        'app': APP,
    }

    driver = webdriver.Remote(APPIUM, CAPS)
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(
            (MobileBy.ACCESSIBILITY_ID, 'Login Screen')))
        driver.find_element(MobileBy.CLASS_NAME, 'android.widget.TextView')
        driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Webview Demo"]')
    finally:
        driver.quit()
       
What do we need to change to make this work on Android? We need some of the Android-specific constants, like the APP and the CAPS constants. The first find command, wrapped up in the WebDriverWait, is the same for both iOS and Android. That's because it's using the Accessibility ID locator strategy, and I know that the developer put the same accessibility ID on both versions of the app. 

The next wait command differs for platforms. Since Android doesn't know anything about <code>XCUIElementType</code> stuff, we change it to omething Android does know about, namely elements of type <code>android.widget.TextView</code>:

    driver.find_element(MobileBy.CLASS_NAME, 'android.widget.TextView')

There are definitely some of these types of views on the page, so that should work. And now, let's use the proper XPath find command as well, since again, the iOS XPath query will not find anything in our Android view hierarchy. Let's try to find the equivalent element using Android node types and attribute names.

    driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Webview Demo"]')

In this case I use the node type <code>android.widget.TextView</code> and attribute <code>text</code>. I know how to do this because I've been able to actually look at the XML source output of the app at this point. You could also try this out by printing the result of the <code>driver.page_source</code> command. Back in the terminal, I run:

    python find_android.py

Or, on macOS

    python3 find_android.py

And since I have a running Appium server and a running emulator, this script will start to run. I'll go over here to the emulator to wait and see my app pop open and then close again. And like before, if there's no output on the command line where I ran my Python script, then that means things worked successfully, and all the elements were able to be found. If you ran into an error and suspect your emulator might be running a bit slow, then you can always bump up the timeout in the WebDriverWait to see if that helps.

Alright, so this is how we use the Appium-specific locator strategies to find elements in our mobile apps! You can already see that dealing with element selectors on multiple platforms can be a bit interesting, if we're not able to use the Accessibility ID strategy.


