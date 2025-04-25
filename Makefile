.PHONY: build clean install

build:
	source chatenv/bin/activate && buildozer -v android debug

install:
	adb install -r bin/*.apk

clean:
	buildozer android clean
	rm -rf bin/ .buildozer

reset:
	rm -rf .buildozer build bin

apk:
	@echo "APK will be here after build: bin/ChatFinanceAssistant-0.1-debug.apk"
