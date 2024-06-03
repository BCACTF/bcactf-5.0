<script>
    import { onDestroy } from 'svelte'
    import { fade } from 'svelte/transition'

    import { page } from '$app/stores'
    import { goto } from '$app/navigation'

    let captchaContainer

    let popover
    let keyContainer

    let cleanupPopover

    let solving = false
    let captchaData = {}

    let word = ''

    let redirectTimeout

    let loading = false
    let errorMessage = ''

    $: destination = $page.url.searchParams.get('destination')

    const repositionPopover = () => {
        FloatingUIDOM.computePosition(keyContainer, popover, {
            placement: 'bottom',
            middleware: [FloatingUIDOM.shift({
                padding: 15
            }), FloatingUIDOM.offset(10)]
        }).then(({ x, y }) => {
            Object.assign(popover.style, {
                left: `${x}px`,
                top: `${y}px`,
            })
        })
    }

    const updateCaptcha = async body => {
        loading = true
        errorMessage = null

        const response = await fetch('/captcha', {
            method: 'POST',
            body: JSON.stringify(body),
            headers: { 'content-type': 'application/json' }
        })

        const json = await response.json().catch(() => ({
            error: response.statusText ?? `Error ${response.status}`
        }))

        loading = false

        if (!response.ok) {
            errorMessage = json.error
            return
        }

        if (json.done) {
            captchaData.captchaToken = json.captchaToken
            captchaData.done = true
        } else {
            captchaData = json
        }
    }

    const startSolving = async () => {
        if (captchaData.done) {
            return
        }

        await updateCaptcha({ routeId: destination })
        solving = true
    }

    const solveChallenge = async () => {
        if (!word.length || captchaData.done) {
            return
        }

        await updateCaptcha({
            captchaToken: captchaData.captchaToken,
            word
        })

        word = ''

        if (captchaData.done) {
            solving = false
            redirectTimeout = setTimeout(() => {
                redirectTimeout = null
                goto(destination + '?token=' + captchaData.captchaToken)
            }, 1_000)
        }
    }

    const bodyClick = event => {
        if (solving && !loading && !captchaContainer.contains(event.target)) {
            solving = false
        }
    }

    $: if (solving && popover && !cleanupPopover) {
        cleanupPopover = FloatingUIDOM.autoUpdate(
            keyContainer,
            popover,
            repositionPopover
        )
    } else if (!solving && cleanupPopover) {
        cleanupPopover()
        cleanupPopover = null
        word = ''
    }

    onDestroy(() => {
        if (cleanupPopover) {
            cleanupPopover()
            cleanupPopover = null
        }

        if (redirectTimeout) {
            clearTimeout(redirectTimeout)
            redirectTimeout = null
        }
    })
</script>

<style>
    @media screen and (max-width: 500px) {
        .main-container {
            padding: 15px !important;
        }
    }

    .captcha-container {
        width: 340px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .key-container {
        line-height: 0;
    }

    .key-btn {
        height: 30px;
        width: 30px;
        border-width: 2px;
        margin-right: 12px;
    }

    .brand-container {
        margin-left: 20px;
        color: gray;
    }

    .captcha-brand {
        font-size: 10px;
    }

    .captcha-popover {
        max-width: unset;
        width: max-content;
        position: absolute;
    }
</style>

<svelte:window on:mousedown={bodyClick} />

<div class="p-5 main-container">
    <h1 class="d-flex align-items-center gap-3 fw-bold">
        <img src="/svg/robot.svg" alt="Robot" />
        Suspicious activity detected!
    </h1>

    <h2 class="fw-light mb-4">
        Please complete the CAPTCHA to access this page.
    </h2>

    <div
        class="p-3 rounded-3 bg-light captcha-container"
        bind:this={captchaContainer}
    >
        <div class="d-flex text-dark">
            <div class="key-container" bind:this={keyContainer}>
                {#if solving}
                    <div class="spinner-border key-btn"></div>
                {:else}
                    <button
                        class="btn btn-outline-dark key-btn"
                        class:btn-outline-dark={!captchaData.done}
                        class:btn-success={captchaData.done}
                        on:click={startSolving}
                    ></button>
                {/if}
            </div>
            <div class="fs-5">I am not a robot.</div>
        </div>

        <div class="d-flex flex-column align-items-center brand-container">
            <img src="/svg/keyhole.svg" alt="Keyhole" />
            <small class="captcha-brand">Fogblaze Captcha</small>
        </div>

        {#if solving}
            <div
                class="popover captcha-popover"
                transition:fade={{ duration: 300 }}
                bind:this={popover}
            >
                <div class="popover-header">CAPTCHA Challenge</div>
                <div class="popover-body">
                    {#if errorMessage}
                        <div class="alert alert-danger mb-0">
                            {errorMessage}
                        </div>
                    {:else}
                        <div class="mb-2">
                            Please solve this challenge to verify your identity.
                        </div>

                        <img
                            src={captchaData.image}
                            alt="CAPTCHA Challenge"
                            class="rounded border d-block"
                        >

                        <div class="d-flex gap-2 mt-2">
                            <input
                                type="text"
                                class="form-control mt-2"
                                placeholder="Answer&hellip;"
                                readonly={loading}
                                bind:value={word}
                            />
                            <button
                                class="btn btn-success mt-2"
                                disabled={loading}
                                on:click={solveChallenge}
                            >Submit</button>
                        </div>

                        <div class="text-muted text-center mt-2">
                            Step {captchaData.solved + 1} of {captchaData.total}
                        </div>
                    {/if}
                </div>
            </div>
        {/if}
    </div>
</div>
