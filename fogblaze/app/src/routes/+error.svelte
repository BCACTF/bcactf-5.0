<script>
    import { page } from '$app/stores'
</script>

<div class="p-3">
    <h1>Error {$page.status}</h1>
    <p>{$page.error.message}</p>
</div>
